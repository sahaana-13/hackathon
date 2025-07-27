from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Order, Supplier, Review, Vendor
from .forms import OrderForm, RegisterForm, ReviewForm, VendorRegistrationForm, ProductForm
from django.contrib.auth.views import LogoutView

# Django REST Framework imports
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ProductSerializer, OrderSerializer


@login_required(login_url='/login/')
def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.select_related('supplier').filter(
            Q(name__icontains=query) |
            Q(supplier__company_name__icontains=query)
        )
    else:
        products = Product.objects.select_related('supplier').all()
    return render(request, 'products.html', {'products': products, 'query': query})


@login_required(login_url='/login/')
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('product_list')
    else:
        form = OrderForm()
    return render(request, 'place_order.html', {'form': form})


@login_required(login_url='/login/')
def order_list(request):
    orders = Order.objects.filter(user=request.user).select_related('product', 'product__supplier').all()
    return render(request, 'orders.html', {'orders': orders})


class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # anyone can see products


class OrderListCreateAPI(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]  # must be logged in to place orders
        return [AllowAny()]  # anyone can view orders


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.GET.get('next', '/products/')  # fallback to /products/ if no next

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)  # redirect after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # redirect to login page after successful registration
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required(login_url='/login/')
def supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    reviews = supplier.reviews.all()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.supplier = supplier
            review.user = request.user
            review.save()
            return redirect('supplier_detail', supplier_id=supplier.id)
    else:
        form = ReviewForm()

    return render(request, 'supplier_detail.html', {
        'supplier': supplier,
        'reviews': reviews,
        'form': form,
    })


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).select_related('product', 'vendor')
    return render(request, 'my_orders.html', {'orders': orders})


@login_required
def add_product(request):
    try:
        vendor = request.user.vendor
        supplier = Supplier.objects.get(vendor=vendor)  # ✅ Get the Supplier linked to this Vendor
    except (Vendor.DoesNotExist, Supplier.DoesNotExist):
        return redirect('become_vendor')  # or show an error

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.supplier = supplier  # ✅ Correctly assign Supplier instance
            product.save()
            return redirect('vendor_dashboard')
    else:
        form = ProductForm()

    return render(request, 'vendor/add_product.html', {'form': form})


@login_required
def vendor_profile(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    products = Product.objects.filter(supplier__vendor=vendor)  # Fixed relation
    return render(request, 'vendor_profile.html', {'vendor': vendor, 'products': products})


@login_required
def vendor_dashboard(request):
    try:
        vendor = request.user.vendor
    except Vendor.DoesNotExist:
        return redirect('become_vendor')

    products = Product.objects.filter(supplier__vendor=vendor)  # Corrected filter
    orders = Order.objects.filter(product__supplier__vendor=vendor)  # Corrected filter

    context = {
        'vendor': vendor,
        'products': products,
        'orders': orders,
    }
    return render(request, 'vendor/dashboard.html', context)


@login_required
def become_vendor(request):
    if hasattr(request.user, 'vendor'):
        # User is already a vendor
        return redirect('vendor_dashboard')

    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.save()
            return redirect('vendor_dashboard')
    else:
        form = VendorRegistrationForm()

    return render(request, 'vendor/become_vendor.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login') 
