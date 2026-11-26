from django.shortcuts import render
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