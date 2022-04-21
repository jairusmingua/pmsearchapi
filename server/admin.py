from django.contrib import admin
from server.models import Song
# Register your models here.

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'isrc',
        'source',
        'artist',
        'external_id',
        'thumbnail_src'
    ]
    search_fields = [
        'title__icontains',
        'isrc',
        'artist__icontains',
        'external_id'
    ]
    list_filter = [
        'source'
    ]
    class Meta:
        model = Song

# class CartAdmin(admin.ModelAdmin):
#     class CartItemAdmin(admin.StackedInline):
#         model = CartItem
#         extra = 0
#         raw_id_fields = ['product']
#         fields = ['product', 'quantity', 'price', '_bill', 'total_amount', 'metadata']

#     inlines = [CartItemAdmin]
#     raw_id_fields = ['customer']
#     fields = ['customer', '_bill', 'total_amount', 'metadata']
#     search_fields = [
#         'customer__customer_code',
#         'customer__user__username',
#         'customer__user__email',
#     ]
