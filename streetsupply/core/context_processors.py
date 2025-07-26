from .models import Vendor

def vendor_status(request):
    is_vendor = False
    if request.user.is_authenticated:
        is_vendor = Vendor.objects.filter(user=request.user).exists()
    return {'is_vendor': is_vendor}
