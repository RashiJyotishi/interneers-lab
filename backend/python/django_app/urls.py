from django.contrib import admin
from django.urls import path
from django_app.adapters.http.product_category_handler import categories, category_detail
from django_app.adapters.http.hello_handler import hello_world
from django_app.adapters.http.product_handler import bulk_create_products, product_category_assign, products, product_detail, products_by_category

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('hello/', hello_world),
    # path('test-mongo/', test_mongo),
    path('hello-world/', hello_world),
    # Products
    path('products/', products),
    path('products/bulk/', bulk_create_products),
    path('products/<str:product_id>/', product_detail),
    path('products/<str:product_id>/category/', product_category_assign),

    # Categories
    path('categories/', categories),
    path('categories/<str:category_id>/', category_detail),
    path('categories/<str:category_id>/products/', products_by_category),
    
]
