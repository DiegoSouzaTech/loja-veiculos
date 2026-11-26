from urllib.parse import quote
from django.conf import settings
from django.shortcuts import redirect, render
from vehicles.models import Vehicle


def home(request):
    featured_vehicles = (
        Vehicle.objects.filter(status=Vehicle.StatusChoices.AVAILABLE, is_featured=True)
        .select_related("brand")
        .prefetch_related("photos")[:6]
    )

    if not featured_vehicles:
        featured_vehicles = (
            Vehicle.objects.filter(status=Vehicle.StatusChoices.AVAILABLE)
            .select_related("brand")
            .prefetch_related("photos")[:6]
        )

    context = {
        "featured_vehicles": featured_vehicles,
    }
    return render(request, "core/home.html", context)


def about(request):
    return render(request, "core/about.html")


def sell_vehicle(request):
    if request.method == "POST":
        owner_name = request.POST.get("owner_name", "").strip()
        owner_phone = request.POST.get("owner_phone", "").strip()
        car_model = request.POST.get("car_model", "").strip()
        car_year = request.POST.get("car_year", "").strip()
        car_mileage = request.POST.get("car_mileage", "").strip()
        notes = request.POST.get("notes", "").strip()

        whatsapp = settings.WHATSAPP_NUMBER
        if whatsapp and owner_name and car_model:
            message = (
                f"Olá! Me chamo *{owner_name}* ({owner_phone}). "
                f"Gostaria de uma avaliação para vender/trocar meu veículo na *{settings.SITE_NAME}*:\n"
                f"• *Veículo:* {car_model}\n"
                f"• *Ano:* {car_year}\n"
                f"• *Quilometragem:* {car_mileage} km"
            )
            if notes:
                message += f"\n• *Observações:* {notes}"

            return redirect(f"https://wa.me/{whatsapp}?text={quote(message)}")

    return render(request, "core/sell_vehicle.html")