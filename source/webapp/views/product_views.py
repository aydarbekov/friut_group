from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView, TemplateView

from webapp.models import Product, Category

import telebot

bot = telebot.TeleBot('1924264594:AAEjo4O0pZnuPlP6IW91j31zpTfzCnaLllQ')
# для нового пользователя
# @bot.message_handler(commands=['start'])
# def start(message):
#     print(message.chat.id)
#     bot.send_message(659261315, 'It works!')
# bot.polling()

# для отправки
# bot = telebot.TeleBot('1924264594:AAEjo4O0pZnuPlP6IW91j31zpTfzCnaLllQ')
# bot.send_message(659261315, 'It works!')


@method_decorator(ensure_csrf_cookie, name='dispatch')
class IndexView(ListView):
    template_name = 'index.html'
    queryset = Category.objects.filter(is_active=True, parent=None).order_by('-updated_at')[:4]
    context_object_name = "hor_categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ver_categories'] = Category.objects.filter(is_active=True, parent=None).order_by('-updated_at')[4:]
        context['populars'] = Product.objects.filter(is_active=True).order_by('-count_sold')[:20]
        context['promos'] = Product.objects.filter(is_active=True, discount__gt=0).order_by('-discount')[:20]
        context['lasts'] = Product.objects.filter(is_active=True).order_by('-updated_at')[:20]
        products = self.request.session.get('products', [])
        context['products_count'] = len(products)
        context['bestseller'] = Product.objects.filter(is_active=True, offer=True).order_by('-updated_at').first()
        return context


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ProductsInCategoryView(ListView):
    template_name = 'products_in_category.html'

    def get_queryset(self):
        category_products = Product.objects.filter(category__slug=self.kwargs['slug']).order_by('name')
        return category_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hor_categories'] = Category.objects.filter(is_active=True, parent=None).order_by('-updated_at')[:4]
        context['ver_categories'] = Category.objects.filter(is_active=True, parent=None).order_by('-updated_at')[4:]
        context['category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        context['products'] = Product.objects.filter(category__in=Category.objects.get(slug=self.kwargs['slug'])
                                                     .get_descendants(include_self=True))
        context['categories'] = Category.objects.all()
        context['parents'] = get_object_or_404(Category, slug=self.kwargs['slug']).get_ancestors(ascending=False, include_self=True)
        products = self.request.session.get('products', [])
        context['products_count'] = len(products)
        return context


class SearchView(ListView):
    template_name = 'products_in_category.html'

    def get_queryset(self):
        category_products = Product.objects.filter(name__icontains=self.request.GET.get('search')).order_by('name')
        return category_products

    def get_context_data(self, **kwargs):
        search = self.request.GET.get('search')
        context = super().get_context_data(**kwargs)
        context['hor_categories'] = Category.objects.filter(is_active=True, parent=None).order_by('-updated_at')[:4]
        context['ver_categories'] = Category.objects.filter(is_active=True, parent=None).order_by('-updated_at')[4:]
        # context['category'] = Category.objects.all()[0]
        context['products'] = Product.objects.filter(name__icontains=search).order_by('name')
        context['categories'] = Category.objects.all()
        # context['parents'] = None
        products = self.request.session.get('products', [])
        context['products_count'] = len(products)
        return context


class AboutView(TemplateView):
    template_name = 'about.html'
