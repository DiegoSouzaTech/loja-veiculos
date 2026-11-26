from django.contrib import admin
from .models import Brand, Vehicle, VehiclePhoto


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class VehiclePhotoInline(admin.TabularInline):
    model = VehiclePhoto
    extra = 3
    fields = ("image", "is_cover", "order")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "brand",
        "model",
        "year_model",
        "price",
        "mileage",
        "status",
        "is_featured",
    )
    list_filter = ("status", "is_featured", "brand", "fuel", "transmission")
    search_fields = ("brand__name", "model", "version", "description")
    list_editable = ("price", "status", "is_featured")
    prepopulated_fields = {"slug": ("model", "year_model")}
    inlines = [VehiclePhotoInline]