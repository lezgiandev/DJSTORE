import uuid
from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files import File
import qrcode
from django.conf import settings
from django.core.validators import MinValueValidator


class Venue(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    balance = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return f"{self.name} ({self.city})"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and not self.qr_code:
            url = f"{settings.QR}/venue/{self.id}/request"
            qr_img = qrcode.make(url)
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            self.qr_code.save(f'qr_{self.id}.png', File(buffer), save=False)
            super().save(update_fields=['qr_code'])


class Genre(models.Model):
    name = models.CharField(max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Track(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='tracks')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    icon = models.CharField(max_length=1000)
    price = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(1)]
    )

    objects = models.Manager()

    def __str__(self):
        return f"{self.title} - {self.artist}"


class TrackRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонен'),
    ]
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    user_fee = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    payment_id = models.CharField(max_length=100, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('deposit', 'Пополнение'),
        ('withdrawal', 'Списание'),
    ]
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    track_request = models.ForeignKey(TrackRequest, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('processing', 'В обработке'),
        ('succeeded', 'Успешно'),
        ('canceled', 'Отменен'),
        ('failed', 'Ошибка')
    ]

    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    yookassa_payout_id = models.CharField(max_length=100, blank=True)
    bank_card_token = models.CharField(max_length=200)
    fee = models.PositiveIntegerField(default=0)

    objects = models.Manager()
