from django.urls import path

from webapp.views.cart_views import CartView, CartChangeView
from webapp.views.product_views import IndexView, ProductsInCategoryView, SearchView, AboutView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<slug:slug>/', ProductsInCategoryView.as_view(), name='category'),
    path('cart/change/', CartChangeView.as_view(), name='cart_change'),
    path('cart/', CartView.as_view(), name='cart'),
    path('search/', SearchView.as_view(), name='search'),
    path('about/', AboutView.as_view(), name='about'),

    # path('article/<int:pk>/', ArticleView.as_view(), name='article_view'),
    # path('article/add/', ArticleCreateView.as_view(), name='article_add'),
    # path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    # path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    # path('article/search/', ArticleSearchView.as_view(), name='article_search'),
    # path('article/search/results/', SearchResultsView.as_view(), name='search_results'),
    # path('comments/', CommentListView.as_view(), name='comment_list'),
    # path('comment/add/', CommentCreateView.as_view(), name='comment_add'),
    # path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    # path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    # path('article/<int:pk>/add-comment/', CommentForArticleCreateView.as_view(), name='article_comment_create')
]



