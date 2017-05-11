
from django.test import TestCase, RequestFactory
import os
import sys
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append('/home/sany/the_test/the_test/the_test')
django.setup()
from product.models import Product, Category
from datetime import datetime, timedelta
from django.urls import reverse
from django.contrib.auth.models import User
from product.views import OnlyView


def create_product(days):
    category = Category.objects.create(name='test', slug='test', description='test')
    time = datetime.now() + timedelta(days=days)
    return Product.objects.create(category=category, name='test', slug='test', description='test',
                                  price=3.4, created_at=time, modified_at=time)


class ProductViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test18', email='test@test.com', password='test12345')

    def test_product_created_more_than_tf_hours_with_no_user(self):
        create_product(days=0)
        response = self.client.get(reverse('product:only'))
        # this one must redirect
        self.assertEqual(response.status_code, 302)

    def test_product_created_more_than_tf_hours_with_user(self):
        request = self.factory.get('/24_only')
        request.user = self.user
        create_product(days=-2)
        response = OnlyView.as_view()(request)
        # must display nothing
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context_data['only_24'], [])

    def test_product_created_less_than_tf_hours_with_user(self):
        request = self.factory.get('/24_only')
        request.user = self.user
        create_product(days=0)
        response = OnlyView.as_view()(request)
        # must display 'test'
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context_data['only_24']), ['<Product: TEST test>'])
