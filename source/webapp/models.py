from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from pytils.translit import translify, slugify


class Category(MPTTModel):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    image = models.ImageField(upload_to='category_images', blank=True, null=True, verbose_name='Изображение')


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = translify(self.name)
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Товар')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание')
    category = models.ForeignKey(Category, null=False, blank=False, related_name='products', on_delete=models.CASCADE,
                                 verbose_name='Категория')
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=4, decimal_places=0, null=False, blank=False, verbose_name='Цена')
    discount = models.IntegerField(verbose_name='Скидка', null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=4, decimal_places=0, null=True, blank=True, verbose_name='Цена со скидкой')
    in_stock = models.BooleanField(verbose_name='В наличии', default=True)
    quantity = models.IntegerField(verbose_name='Количество', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    offer = models.BooleanField(verbose_name='Акция', default=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    count_sold = models.IntegerField(default=0, verbose_name='Кол-во проданных')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def save(self, *args, **kwargs):
        value = translify(self.name)
        self.slug = slugify(value)
        if self.discount and self.discount != 0:
            self.discounted_price = self.price - (self.price * self.discount / 100)
        elif not self.discount and self.discounted_price:
            self.discounted_price = None
        super().save(*args, **kwargs)


class Image(models.Model):
    image = models.ImageField(upload_to='product_images', verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='фотографии')

    def _str_(self):
        return self.product

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Order(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(max_length=50, null=True, blank=True, verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=255, null=False, blank=False, verbose_name="Адрес доставки")
    shipping_district = models.ForeignKey('DeliveryDistricts', on_delete=models.PROTECT, verbose_name="Район доставки", null=True, blank=True, default=None)
    products = models.ManyToManyField(Product, through='OrderProduct', through_fields=('order', 'product'), verbose_name='Товары', related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    additional_info = models.CharField(max_length=255, null=True, blank=True, verbose_name="Коментарий к заказу")
    total_sum = models.DecimalField(max_digits=9, decimal_places=2, default=9999)

    def __str__(self):
        return "{} {} {} {}".format(self.first_name, self.last_name, self.phone, self.created_at, self.total_sum)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    # def save(self, *args, **kwargs):
    #     products = self.products
    #     summ = 0
    #     print(products)
    #     # for product in products:
    #     #     if product.product.discounted_price:
    #     # if self.discount and self.discount != 0:
    #     #     self.discounted_price = self.price - (self.price * self.discount / 100)
    #     # elif not self.discount and self.discounted_price:
    #     #     self.discounted_price = None
    #     super().save(*args, **kwargs)


class DeliveryDistricts(models.Model):
    district = models.CharField(max_length=255, null=False, blank=False, verbose_name='Район')
    price = models.DecimalField(max_digits=4, decimal_places=0, null=False, blank=False, verbose_name='Цена')

    def __str__(self):
        return f'{self.district} - {self.price}'

    class Meta:
        verbose_name = 'Район доставки'
        verbose_name_plural = 'Районы доставки'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderproduct", verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orderproduct", verbose_name='Товар')
    amount = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.product.name} {self.order}'

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'

