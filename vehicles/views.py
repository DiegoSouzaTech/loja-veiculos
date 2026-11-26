from django.shortcuts import get_object_or_404, render
from .models import Brand, Vehicle


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
    context = {
        "vehicle": vehicle,
    }
    return render(request, "vehicles/vehicle_detail.html", context)