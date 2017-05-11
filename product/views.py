from django.views import generic
from .models import Category, Product
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta
import operator
from functools import reduce
from django.db.models import Q


class IndexView(generic.TemplateView):
    template_name = 'product/index.html'


class CategoryView(generic.ListView):
    template_name = 'product/category_list.html'
    context_object_name = 'categories'
    paginate_by = 4

    def get_queryset(self):
        return Category.objects.all()


class ProductView(generic.ListView):
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        category = Category.objects.filter(slug=self.kwargs['slug'])
        return Product.objects.filter(category=category)


class TheProductView(generic.DetailView):
    model = Product
    template_name = 'product/the_product.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_pr'


class OnlyView(LoginRequiredMixin, generic.ListView):
    template_name = 'product/only_24.html'
    context_object_name = 'only_24'
    login_url = '/accounts/login/'
    paginate_by = 4

    def get_queryset(self):
        time_delta = datetime.now() - timedelta(hours=24)
        return Product.objects.filter(created_at__gte=time_delta)


class ProductSearchListView(generic.ListView):
    template_name = 'product/search_res.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        result = Product.objects.all()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list))
            )
        return result
