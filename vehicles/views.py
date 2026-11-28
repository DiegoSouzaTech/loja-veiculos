from urllib.parse import quote
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from .models import Brand, Lead, Vehicle
from django.utils.formats import number_format


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

    if request.method == "POST" and vehicle.status == Vehicle.StatusChoices.AVAILABLE:
        name = request.POST.get("name", "").strip()[:100]
        phone = request.POST.get("phone", "").strip()[:25]
        intent = request.POST.get("intent", Lead.IntentChoices.FINANCING)
        valid_intents = {choice[0] for choice in Lead.IntentChoices.choices}
        if intent not in valid_intents:
            intent = Lead.IntentChoices.FINANCING

        if name and phone:
            lead = Lead.objects.create(
                vehicle=vehicle,
                name=name,
                phone=phone,
                intent=intent,
            )
            intent_label = dict(Lead.IntentChoices.choices).get(intent, intent)
            preco = number_format(vehicle.price, decimal_pos=2, force_grouping=True)
            message = (
                f"Olá! Me chamo *{lead.name}*. "
                f"Vi o *{vehicle}* (R$ {preco}) no site da *{settings.SITE_NAME}*: "
                f"{request.build_absolute_uri()} "
                f"e gostaria de falar sobre: _{intent_label}_."
            )
            whatsapp_url = f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={quote(message)}"
            return redirect(whatsapp_url)

    context = {
        "vehicle": vehicle,
        "intent_choices": Lead.IntentChoices.choices,
        "whatsapp_number": settings.WHATSAPP_NUMBER,
    }
    return render(request, "vehicles/vehicle_detail.html", context)