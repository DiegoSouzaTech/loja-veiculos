from urllib.parse import quote
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from .models import Brand, Lead, Vehicle


def vehicle_list(request):
    vehicles = (
        Vehicle.objects.filter(status=Vehicle.StatusChoices.AVAILABLE)
        .select_related("brand")
        .prefetch_related("photos")
    )
    brands = Brand.objects.all()

    brand_slug = request.GET.get("marca")
    query = request.GET.get("q")

    if brand_slug:
        vehicles = vehicles.filter(brand__slug=brand_slug)

    if query:
        vehicles = vehicles.filter(model__icontains=query)

    context = {
        "vehicles": vehicles,
        "brands": brands,
        "selected_brand": brand_slug,
        "query": query or "",
    }
    return render(request, "vehicles/vehicle_list.html", context)


def vehicle_detail(request, slug):
    vehicle = get_object_or_404(
        Vehicle.objects.select_related("brand").prefetch_related("photos"),
        slug=slug,
    )

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        intent = request.POST.get("intent", Lead.IntentChoices.INTEREST)

        if name and phone:
            lead = Lead.objects.create(
                vehicle=vehicle,
                name=name,
                phone=phone,
                intent=intent,
            )

            whatsapp = settings.WHATSAPP_NUMBER
            if whatsapp:
                intent_label = lead.get_intent_display()
                message = (
                    f"Olá! Me chamo *{name}*. "
                    f"Vi o *{vehicle}* (R$ {vehicle.price}) no site da *{settings.SITE_NAME}* "
                    f"e gostaria de falar sobre: _{intent_label}_."
                )
                return redirect(f"https://wa.me/{whatsapp}?text={quote(message)}")

            return redirect("vehicles:detail", slug=vehicle.slug)

    context = {
        "vehicle": vehicle,
        "intent_choices": Lead.IntentChoices.choices,
    }
    return render(request, "vehicles/vehicle_detail.html", context)