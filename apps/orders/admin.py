from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'price', 'quantity', 'subtotal_display']
    fields = ['product_name', 'price', 'quantity', 'subtotal_display']

    def subtotal_display(self, obj):
        return f"KES {obj.subtotal:,.0f}"
    subtotal_display.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'status', 'status_badge', 'total_display', 'created_at']    
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'phone', 'email', 'delivery_address']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'total']
    inlines = [OrderItemInline]

    def total_display(self, obj):
        return f"KES {obj.total:,.0f}"
    total_display.short_description = 'Total'

    def status_badge(self, obj):
        colors = {
            'pending': ('#FAEEDA', '#633806'),
            'confirmed': ('#E6F1FB', '#0C447C'),
            'processing': ('#EEEDFE', '#3C3489'),
            'shipped': ('#E1F5EE', '#085041'),
            'delivered': ('#EAF3DE', '#27500A'),
            'cancelled': ('#FCEBEB', '#791F1F'),
        }
        bg, color = colors.get(obj.status, ('#F1EFE8', '#444441'))
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;border-radius:99px;font-size:12px">{}</span>',
            bg, color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
