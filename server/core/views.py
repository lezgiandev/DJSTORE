from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from django.db import transaction as db_transaction
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from yookassa import Payment, Payout
from .serializers import *
from .models import Venue, TrackRequest, Transaction, WithdrawalRequest
from .services import create_yookassa_payment, create_card_token, create_yookassa_payout


class VenueView(generics.RetrieveUpdateAPIView):
    serializer_class = VenueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Venue, user=self.request.user)


class VenueRegistrationView(generics.CreateAPIView):
    serializer_class = VenueRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class GenresView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class VenueTrackListView(generics.ListCreateAPIView):
    serializer_class = TrackSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['genre']
    search_fields = ['title', 'artist']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        venue_id = self.kwargs.get('venue_id')
        return Track.objects.filter(venue_id=venue_id)

    def perform_create(self, serializer):
        serializer.save(venue=self.request.user.venue)


class TrackDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'track_id'

    def get_queryset(self):
        return Track.objects.filter(venue__user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.venue.user != self.request.user:
            raise permissions.exceptions.PermissionDenied("Вы не являетесь владельцем этого трека")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.venue.user != self.request.user:
            raise permissions.exceptions.PermissionDenied("Вы не можете удалить чужой трек")
        instance.delete()


class TrackRequestCreateView(generics.CreateAPIView):
    serializer_class = TrackRequestSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['venue_id'] = self.kwargs['venue_id']
        return context

    @db_transaction.atomic
    def perform_create(self, serializer):
        venue = get_object_or_404(Venue, pk=self.kwargs['venue_id'])
        track = get_object_or_404(Track, pk=self.request.data['track'], venue=venue)
        serializer.save(track=track)


class MockPaymentView(APIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request, payment_token):  # Добавляем обработчик GET
        track_request = get_object_or_404(
            TrackRequest,
            payment_token=payment_token
        )
        serializer = TrackRequestSerializer(track_request)
        return Response(serializer.data)

    @staticmethod
    def post(request, payment_token):
        with db_transaction.atomic():
            track_request = get_object_or_404(
                TrackRequest,
                payment_token=payment_token
            )

            if track_request.is_paid:
                return Response(
                    {"detail": "Запрос уже оплачен"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            track_request.is_paid = True
            track_request.save()

            # Убрано начисление средств на баланс заведения
            return Response(
                {"detail": "Оплата успешно подтверждена"},
                status=status.HTTP_200_OK
            )


class WithdrawalView(generics.CreateAPIView):
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]

    @db_transaction.atomic
    def perform_create(self, serializer):
        venue = self.request.user.venue
        amount = serializer.validated_data['amount']
        fee_percent = getattr(settings, 'WITHDRAWAL_FEE_PERCENT', 0.05)
        fee = int(amount * fee_percent)

        locked_venue = Venue.objects.select_for_update().get(pk=venue.pk)
        if locked_venue.balance < amount:
            raise ValidationError("Недостаточно средств на балансе")

        card_token = create_card_token({
            'number': serializer.validated_data['card_number'],
            'expiry_year': serializer.validated_data['card_expiry_year'],
            'expiry_month': serializer.validated_data['card_expiry_month'],
            'csc': serializer.validated_data['card_csc']
        })

        payout = create_yookassa_payout(amount, fee, card_token)

        withdrawal = WithdrawalRequest.objects.create(
            venue=venue,
            amount=amount,
            bank_card_token=card_token,
            fee=fee,
            yookassa_payout_id=payout.id,
            status='processing'
        )

        locked_venue.balance = F('balance') - amount
        locked_venue.save()

        Transaction.objects.create(
            venue=venue,
            amount=-amount,
            transaction_type='withdrawal'
        )


class MockWithdrawalView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @db_transaction.atomic
    def post(self, request):
        serializer = WithdrawalSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        venue = request.user.venue
        amount = serializer.validated_data['amount']
        fee_percent = getattr(settings, 'WITHDRAWAL_FEE_PERCENT', 0.05)
        fee = int(amount * fee_percent)

        locked_venue = Venue.objects.select_for_update().get(pk=venue.pk)
        if locked_venue.balance < amount:
            return Response(
                {"detail": "Недостаточно средств на балансе"},
                status=status.HTTP_400_BAD_REQUEST
            )

        withdrawal = WithdrawalRequest.objects.create(
            venue=venue,
            amount=amount,
            bank_card_token='mock_card_token',
            fee=fee,
            yookassa_payout_id=f'mock_payout_{uuid.uuid4()}',
            status='succeeded'
        )

        # Обновляем баланс
        locked_venue.balance = F('balance') - amount
        locked_venue.save()

        Transaction.objects.create(
            venue=venue,
            amount=-amount,
            transaction_type='withdrawal',
        )

        return Response({
            "id": withdrawal.id,
            "amount": amount,
            "fee": fee,
            "status": "succeeded"
        }, status=status.HTTP_201_CREATED)


class WithdrawalWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def post(request):
        payout = Payout.find_one(request.data['object']['id'])

        withdrawal = WithdrawalRequest.objects.get(
            yookassa_payout_id=payout.id
        )

        if payout.status == 'succeeded':
            withdrawal.status = 'succeeded'
        elif payout.status == 'canceled':
            withdrawal.status = 'canceled'

            Venue.objects.filter(pk=withdrawal.venue.pk).update(
                balance=F('balance') + withdrawal.amount
            )
        else:
            withdrawal.status = payout.status

        withdrawal.save()
        return Response(status=status.HTTP_200_OK)


class TrackRequestListView(generics.ListAPIView):
    serializer_class = TrackRequestSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return TrackRequest.objects.filter(
            track__venue=self.request.user.venue
        ).select_related('track')


class TrackRequestUpdateView(generics.UpdateAPIView):
    serializer_class = TrackRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return TrackRequest.objects.filter(
            track__venue=self.request.user.venue
        ).select_related('track')

    @db_transaction.atomic
    def perform_update(self, serializer):
        instance = self.get_object()
        new_status = serializer.validated_data.get('status')

        if instance.status != 'pending':
            raise ValidationError("Можно изменять только ожидающие запросы")

        if new_status == 'accepted' and not instance.is_paid:
            raise ValidationError("Запрос должен быть оплачен перед принятием")

        serializer.save()

        if new_status == 'accepted':
            with db_transaction.atomic():
                venue = Venue.objects.select_for_update().get(pk=instance.track.venue.pk)
                venue.balance = F('balance') + instance.user_fee
                venue.save()

                Transaction.objects.create(
                    venue=venue,
                    amount=instance.user_fee,
                    transaction_type='deposit',
                    track_request=instance
                )


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            venue=self.request.user.venue
        ).order_by('-created_at')


class WithdrawalListView(generics.ListAPIView):
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WithdrawalRequest.objects.filter(
            venue=self.request.user.venue
        ).order_by('-created_at')


class PaymentCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    @db_transaction.atomic
    def post(self, request, *args, **kwargs):
        track_request = get_object_or_404(
            TrackRequest,
            payment_token=kwargs['payment_token'],
            track__venue=request.user.venue
        )

        payment = create_yookassa_payment(
            amount=track_request.user_fee,
            payment_token=track_request.payment_token,
            description=f"Оплата трека {track_request.track.title}"
        )

        track_request.payment_id = payment.id
        track_request.save()

        return Response({
            'confirmation_url': payment.confirmation.confirmation_url
        }, status=status.HTTP_201_CREATED)


class PaymentWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def post(request):
        payment = Payment.find_one(request.data['object']['id'])
        if payment.status == 'succeeded':
            with db_transaction.atomic():
                track_request = TrackRequest.objects.select_for_update().get(
                    payment_token=payment.metadata['payment_token']
                )
                if track_request.is_paid:
                    return Response(status=status.HTTP_200_OK)

                track_request.is_paid = True
                track_request.transaction_id = payment.id
                track_request.save()

                venue = track_request.track.venue
                Venue.objects.filter(pk=venue.pk).update(
                    balance=F('balance') + track_request.user_fee
                )
                Transaction.objects.create(
                    venue=venue,
                    amount=track_request.user_fee,
                    transaction_type='deposit',
                    track_request=track_request
                )
        return Response(status=status.HTTP_200_OK)
