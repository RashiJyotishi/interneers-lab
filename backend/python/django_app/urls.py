from django.contrib import admin
from django.urls import path
from django_app.adapters.http.hello_handler import hello_world
from django_app.adapters.http.product_handler import products, product_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('hello/', hello_world),
    # path('test-mongo/', test_mongo),
    path('hello-world/', hello_world),
    path('products/', products),
    path('products/<str:product_id>/', product_detail),
]
