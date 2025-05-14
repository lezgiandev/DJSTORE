from django.contrib import admin
from .models import *

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'city', 'phone', 'balance')
    search_fields = ('name', 'city', 'user__username')
    readonly_fields = ('qr_code', 'balance')
    list_filter = ('city',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'venue', 'genre', 'icon', 'price')
    search_fields = ('title', 'artist', 'venue__name')
    list_filter = ('genre', 'venue__city')
    raw_id_fields = ('venue', 'genre')


@admin.register(TrackRequest)
class TrackRequestAdmin(admin.ModelAdmin):
    list_display = ('track', 'user_fee', 'status', 'is_paid', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('track__title', 'track__artist')
    raw_id_fields = ('track',)
    readonly_fields = ('created_at', 'transaction_id')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('venue', 'amount', 'transaction_type', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('venue__name',)
    raw_id_fields = ('venue', 'track_request')
    readonly_fields = ('created_at',)


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('venue', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('venue__name',)
    raw_id_fields = ('venue',)
    readonly_fields = ('created_at',)
