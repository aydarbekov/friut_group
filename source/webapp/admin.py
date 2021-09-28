from django.contrib import admin

from webapp.models import Image, Product, Category, Order, DeliveryDistricts, OrderProduct


class Images(admin.TabularInline):
    model = Image
    fields = ['image', 'product']


class ProductsAdmin(admin.ModelAdmin):
    inlines = [Images]
    # exclude = ['slug']


class CategoryProductInline(admin.TabularInline):
    model = Product
    fields = ('name', 'price')
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    exclude = ['slug']
    ordering = ('-updated_at',)

    inlines = (CategoryProductInline,)

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    fields = ('product', 'amount')
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    # list_display = ('first_name', 'last_name', 'phone', 'email', 'created_at')
    # list_filter = ('status',)
    inlines = (OrderProductInline,)


admin.site.register(Product, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(DeliveryDistricts)
admin.site.register(OrderProduct)