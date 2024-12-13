from django.urls import path
from . import views
from .views import brand_list


urlpatterns = [
    path('brand-list/',views.brand_list,name='brand_list'),
    path('product-list/',views.product_list,name='product_list'),
    path('product-details/<int:id>/',views.product_details,name='product_details'),
    path('update-product/<int:id>/',views.update_product,name='update_product'),
    path('delete-product/<int:id>/',views.product_details,name='delete_product'),
    path('add-product',views.AddProduct.as_view(),name='add_product'),
    path('add-product-with-django-form',views.add_product_with_django_form,name='add_product_with_django_form'),
    path('add-brand',views.add_brand, name='add_brand'),
]