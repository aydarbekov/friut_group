import json

import telebot
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import CreateView
from django.views.generic.base import View, TemplateView

from webapp.forms import OrderCreateForm
from webapp.models import Product, Order, OrderProduct, DeliveryDistricts


def get_product_summ(pk, products):
    count_product = 0
    product_summ = 0
    if pk in products:
        for i in products:
            if i == pk:
                count_product += 1
        product = Product.objects.get(pk=int(pk))
        if not product.discount:
            product_summ = product.price * count_product
        else:
            product_summ = product.discounted_price * count_product
    return product_summ


def get_totals(products):
    totals = {}
    for product_pk in products:
        if product_pk not in totals:
            totals[product_pk] = 0
        totals[product_pk] += 1
    return totals


def get_cart_total_summ(totals):
    cart_total = 0
    for pk, qty in totals.items():
        product = Product.objects.get(pk=int(pk))
        if not product.discount:
            total = product.price * qty
        else:
            total = product.discounted_price * qty
        cart_total += total
    return cart_total


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CartChangeView(View):

    def post(self, request, *args, **kwargs):
        products = request.session.get('products', [])
        pk = int(request.POST.get('pk'))
        action = request.POST.get('action')
        if action == 'add':
            count = int(request.POST.get('count'))
            for i in range(count):
                products.append(pk)
        elif action == 'remove':
            while pk in products:
                products.remove(pk)
        elif action == 'minus':
            for product_pk in products:
                if product_pk == pk:
                    products.remove(product_pk)
                    break
        else:
            answer = {
                'status': 'Action not allowed',
            }
            return JsonResponse(answer)

        product_summ = get_product_summ(pk, products)
        totals = get_totals(products)
        cart_total = get_cart_total_summ(totals)
        request.session['products'] = products
        request.session['products_count'] = len(products)
        answer = {
            'status': 'success',
            'product_summ': product_summ,
            'products_count': len(products),
            'total': cart_total,
        }
        return JsonResponse(answer)


class CartView(CreateView):
    model = Order
    fields = ('first_name', 'last_name', 'phone', 'email', 'address', 'additional_info', 'shipping_district')
    template_name = 'cart.html'
    success_url = reverse_lazy('webapp:index')

    def get_context_data(self, **kwargs):
        cart, cart_total = self._prepare_cart()
        kwargs['deliveries'] = DeliveryDistricts.objects.all()
        kwargs['cart'] = cart
        kwargs['cart_total'] = cart_total

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if self._cart_empty():
            form.add_error(None, 'В корзине отсутствуют товары!')
            return self.form_invalid(form)
        response = super().form_valid(form)
        self._save_order_products()

        prods = self.object.orderproduct.all()
        sum = 0
        for prod in prods:
            if prod.product.discounted_price:
                sum += prod.product.discounted_price * prod.amount
            else:
                sum += prod.product.price * prod.amount
        self.object.total_sum = sum
        self.object.save()

        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        mail = form.cleaned_data['email']
        address = form.cleaned_data['address']
        additional_info = form.cleaned_data['additional_info']
        shipping_district = form.cleaned_data['shipping_district']
        bot = telebot.TeleBot('1924264594:AAEjo4O0pZnuPlP6IW91j31zpTfzCnaLllQ')
        text = f'''
                !!!Новый заказ!!!
ФИО - {last_name} {first_name}
Номер - {phone}
Почта - {mail}
Адрес - {address}
Комментарий - {additional_info}
Район, цена доставки - {shipping_district}
'''
        cart, cart_total = self._prepare_cart()
        cart_items = ''
        for item in cart:
            cart_items += f"\n {item['product']} - {item['qty']}(шт/кг) * {item['price']}р. = {item['total']}"
        itogo = f'\nИТОГО - {cart_total}'
        self._clean_cart()
        bot.send_message(659261315, text + cart_items + itogo)
        messages.success(self.request, 'Заказ сохранён!\n С вами свяжутся для подтверждения заказа')
        return response

    def _prepare_cart(self):
        totals = self._get_totals()
        cart = []
        cart_total = 0
        for pk, qty in totals.items():
            product = Product.objects.get(pk=int(pk))
            if product.discounted_price:
                price = product.discounted_price
                total = product.discounted_price * qty
            else:
                price = product.price
                total = product.price * qty
            cart_total += total
            cart.append({'product': product, 'qty': qty, 'price': price, 'total': total})
        return cart, cart_total

    def _get_totals(self):
        products = self.request.session.get('products', [])
        totals = {}
        for product_pk in products:
            if product_pk not in totals:
                totals[product_pk] = 0
            totals[product_pk] += 1
        return totals

    def _cart_empty(self):
        products = self.request.session.get('products', [])
        return len(products) == 0

    def _save_order_products(self):
        totals = self._get_totals()
        for pk, qty in totals.items():
            OrderProduct.objects.create(product_id=pk, order=self.object, amount=qty)

    def _clean_cart(self):
        if 'products' in self.request.session:
            self.request.session.pop('products')
