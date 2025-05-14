from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if hasattr(user, 'venue'):
            token['venue_id'] = user.venue.id
        return token


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        source='genre',
        write_only=True
    )

    class Meta:
        model = Track
        fields = ['id', 'title', 'icon', 'genre', 'genre_id', 'artist', 'price']


class TrackRequestSerializer(serializers.ModelSerializer):
    min_fee = serializers.SerializerMethodField()
    track = TrackSerializer(read_only=True)
    payment_url = serializers.SerializerMethodField()

    @staticmethod
    def get_min_fee(obj):
        return obj.track.price

    def validate_user_fee(self, value):
        track_id = self.initial_data.get('track')
        venue_id = self.context.get('venue_id')

        if not track_id or not venue_id:
            raise serializers.ValidationError("Недостаточно данных для создания запроса")

        try:
            track = Track.objects.get(pk=track_id, venue_id=venue_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Указанный трек не добавлен в данное заведение")

        if value < track.price:
            raise serializers.ValidationError(
                f"Сумма должна быть не меньше {track.price}"
            )
        return value

    @staticmethod
    def get_payment_url(obj):
        if obj.payment_id:
            return f"{settings.DOMAIN}/api/payments/process/{obj.payment_token}/"
        return None

    class Meta:
        model = TrackRequest
        fields = ['id', 'payment_url', 'track', 'user_fee', 'status', 'is_paid', 'payment_token', 'created_at', 'min_fee', 'payment_id']
        read_only_fields = ['payment_url', 'is_paid', 'payment_token', 'created_at', 'min_fee']


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'city', 'phone', 'qr_code', 'balance']
        read_only_fields = ['qr_code', 'balance']


class VenueRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(required=True, write_only=True)
    city = serializers.CharField(required=True, write_only=True)
    phone = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name', 'city', 'phone']
        extra_kwargs = {'email': {'required': True}}

    @transaction.atomic
    def create(self, validated_data):
        profile_data = {
            'name': validated_data.pop('name'),
            'city': validated_data.pop('city'),
            'phone': validated_data.pop('phone')
        }
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        venue = Venue.objects.create(user=user, **profile_data)
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if hasattr(instance, 'venue'):
            representation.update({
                'name': instance.venue.name,
                'city': instance.venue.city,
                'phone': instance.venue.phone
            })
        return representation


class WithdrawalSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(
        write_only=True,
        max_length=16,
        required=False,
        allow_blank=True
    )
    card_expiry_year = serializers.CharField(
        write_only=True,
        max_length=4,
        required=False,
        allow_blank=True
    )
    card_expiry_month = serializers.CharField(
        write_only=True,
        max_length=2,
        required=False,
        allow_blank=True
    )
    card_csc = serializers.CharField(
        write_only=True,
        max_length=4,
        required=False,
        allow_blank=True
    )

    class Meta:
        model = WithdrawalRequest
        fields = [
            'amount',
            'card_number',
            'card_expiry_year',
            'card_expiry_month',
            'card_csc',
            'status',
            'created_at',
            'fee'
        ]
        read_only_fields = ['status', 'created_at', 'fee']

    def validate(self, attrs):
        if 'mock-withdraw' in self.context['request'].path:
            return attrs

        required_fields = ['card_number', 'card_expiry_year', 'card_expiry_month', 'card_csc']
        if any(field not in attrs or not attrs[field] for field in required_fields):
            raise serializers.ValidationError("Необходимо указать все данные карты")

        return attrs

    @staticmethod
    def validate_amount(value):
        min_withdrawal = getattr(settings, 'MIN_WITHDRAWAL_AMOUNT', 500)
        if value < min_withdrawal:
            raise serializers.ValidationError(
                f"Минимальная сумма вывода: {min_withdrawal} руб."
            )
        return value


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'created_at']
