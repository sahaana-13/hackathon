from django.urls import path, include
from django.shortcuts import redirect
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', lambda request: redirect('product_list'), name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login', http_method_names=['get', 'post']), name='logout'),
    path('register/', views.register_view, name='register'),
    path('products/', views.product_list, name='product_list'),
    path('order/', views.place_order, name='place_order'),
    path('orders/', views.order_list, name='order_list'),
    path('api/products/', views.ProductListAPI.as_view(), name='api_products'),
    path('api/orders/', views.OrderListCreateAPI.as_view(), name='api_orders'),
    path('api-auth/', include('rest_framework.urls')),
    path('supplier/<int:supplier_id>/', views.supplier_detail, name='supplier_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('add-product/', views.add_product, name='add_product'),
    path('vendor/<int:vendor_id>/', views.vendor_profile, name='vendor_profile'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/add-product/', views.add_product, name='add_product'),
    path('become-vendor/', views.become_vendor, name='become_vendor'),
]
