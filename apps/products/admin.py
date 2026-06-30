from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'category', 'formatted_price', 'stock', 'stock_status_badge', 'is_active']
    list_display_links = ['name']
    list_filter = ['category', 'is_active', 'size']
    search_fields = ['name', 'description']
    list_editable = ['stock', 'is_active']
    readonly_fields = ['image_preview_large', 'created_at', 'updated_at']
    fieldsets = (
        ('Product info', {
            'fields': ('name', 'description', 'category', 'size')
        }),
        ('Pricing & stock', {
            'fields': ('price', 'stock', 'is_active')
        }),
        ('Image', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:48px;height:48px;object-fit:cover;border-radius:6px;">',
                obj.image.url
            )
        return format_html('<span style="color:#aaa;">No image</span>')
    image_preview.short_description = 'Photo'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:300px;max-height:300px;object-fit:contain;border-radius:8px;border:1px solid #eee;">',
                obj.image.url
            )
        return 'No image uploaded yet.'
    image_preview_large.short_description = 'Current image'

    def stock_status_badge(self, obj):
        colors = {
            'in_stock': ('green', '#EAF3DE', '#27500A'),
            'low_stock': ('amber', '#FAEEDA', '#633806'),
            'out_of_stock': ('red', '#FCEBEB', '#791F1F'),
        }
        labels = {
            'in_stock': f'{obj.stock} in stock',
            'low_stock': f'Only {obj.stock} left',
            'out_of_stock': 'Out of stock',
        }
        _, bg, color = colors[obj.stock_status]
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;border-radius:99px;font-size:12px">{}</span>',
            bg, color, labels[obj.stock_status]
        )
    stock_status_badge.short_description = 'Status'

    def formatted_price(self, obj):
        return obj.formatted_price
    formatted_price.short_description = 'Price'
    formatted_price.admin_order_field = 'price'
