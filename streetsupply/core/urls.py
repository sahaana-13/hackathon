# core/urls.py
from django.urls import path, include
from . import views
from .views import ProductListAPI, OrderListCreateAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,

)
from .views import login_view
from .views import register_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect



urlpatterns = [
    path('', lambda request: redirect('product_list'), name='home'),
    path('products/', views.product_list, name='product_list'),
    
    path('order/', views.place_order, name='place_order'),
    path('orders/', views.order_list, name='order_list'),
    path('api/products/', ProductListAPI.as_view(), name='api_products'),
    path('api/orders/', OrderListCreateAPI.as_view(), name='api_orders'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # to get token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # to refresh token
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('supplier/<int:supplier_id>/', views.supplier_detail, name='supplier_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('add-product/', views.add_product, name='add_product'),
    path('vendor/<int:vendor_id>/', views.vendor_profile, name='vendor_profile'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('become-vendor/', views.become_vendor, name='become_vendor'),
    path('vendor/add-product/', views.add_product, name='add_product'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
   




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
