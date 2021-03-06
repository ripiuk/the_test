from django.conf.urls import url
from . import views

app_name = 'product'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^products/$', views.CategoryView.as_view(), name='category'),
    url(r'^products/(?P<slug>[\w-]+)/$', views.ProductView.as_view(), name='product'),
    url(r'^products/(?P<slug>[\w-]+)/(?P<slug_pr>[\w-]+)$', views.TheProductView.as_view(), name='the_product'),
    url(r'^24_only/$', views.OnlyView.as_view(), name='only'),
    url(r'^search_result/?$', views.ProductSearchListView.as_view(), name='product_search'),
]