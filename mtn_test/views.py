import uuid
from django.shortcuts import get_object_or_404, render
from mtn_test.models import Route
from .mtn_payment import MTNMoMoPayment
from django.http import JsonResponse
from .models import Route, Payment


# Create your views here.
def home(request):
    routes = Route.objects.all()
    context = {
        "routes":routes,
    }
    return render(request, 'index.html',context)

def checkout(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    context = {
        "route":route
    }
    return render(request, 'checkout.html',context)

def initiate_payment(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    phone_number = request.POST.get("phone_number")

    if not phone_number:
        return JsonResponse({"error": "Phone number is required"}, status=400)

    transaction_id = str(uuid.uuid4())
    payment = Payment.objects.create(
        route=route,
        phone_number=phone_number,
        amount=route.price,
        transaction_id=transaction_id,
    )

    mtn_payment = MTNMoMoPayment(api_key="your_api_key", subscription_key="your_subscription_key", user_id="your_user_id")
    
    try:
        if mtn_payment.initiate_payment(phone_number, route.price, transaction_id):
            payment.status = "success"
        else:
            payment.status = "failed"
    except Exception as e:
        payment.status = "failed"
        print(f"Payment error: {e}")

    payment.save()
    return JsonResponse({"status": payment.status})
