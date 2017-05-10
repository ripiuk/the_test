from django.views import generic
from .models import Category, Product


class IndexView(generic.TemplateView):
    template_name = 'product/index.html'


class CategoryView(generic.ListView):
    template_name = 'product/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()


class ProductView(generic.ListView):
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = Category.objects.filter(slug=self.kwargs['slug'])
        return Product.objects.filter(category=category)


class TheProductView(generic.DetailView):
    model = Product
    template_name = 'product/the_product.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug_pr'
