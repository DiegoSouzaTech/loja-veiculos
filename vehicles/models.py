from django.db import models
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField("Nome", max_length=60, unique=True)
    slug = models.SlugField("Slug", max_length=80, unique=True, blank=True)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Vehicle(models.Model):
    class FuelChoices(models.TextChoices):
        FLEX = "flex", "Flex"
        GASOLINE = "gasolina", "Gasolina"
        ETHANOL = "etanol", "Etanol"
        DIESEL = "diesel", "Diesel"
        HYBRID = "hibrido", "Híbrido"
        ELECTRIC = "eletrico", "Elétrico"

    class TransmissionChoices(models.TextChoices):
        AUTOMATIC = "automatico", "Automático"
        MANUAL = "manual", "Manual"
        CVT = "cvt", "CVT"
        AUTOMATED = "automatizado", "Automatizado"

    class StatusChoices(models.TextChoices):
        AVAILABLE = "disponivel", "Disponível"
        RESERVED = "reservado", "Reservado"
        SOLD = "vendido", "Vendido"

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="vehicles",
        verbose_name="Marca",
    )
    model = models.CharField("Modelo", max_length=80)
    version = models.CharField("Versão", max_length=100, blank=True)
    slug = models.SlugField("Slug", max_length=220, unique=True, blank=True)

    year_manufacture = models.PositiveIntegerField("Ano de Fabricação")
    year_model = models.PositiveIntegerField("Ano do Modelo")
    mileage = models.PositiveIntegerField("Quilometragem (km)", default=0)
    fuel = models.CharField(
        "Combustível",
        max_length=20,
        choices=FuelChoices.choices,
        default=FuelChoices.FLEX,
    )
    transmission = models.CharField(
        "Câmbio",
        max_length=20,
        choices=TransmissionChoices.choices,
        default=TransmissionChoices.AUTOMATIC,
    )
    color = models.CharField("Cor", max_length=40)
    plate_ending = models.CharField("Final da Placa", max_length=1, blank=True)

    price = models.DecimalField("Preço (R$)", max_digits=10, decimal_places=2)
    description = models.TextField("Descrição / Opcionais", blank=True)
    status = models.CharField(
        "Status",
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.AVAILABLE,
    )
    is_featured = models.BooleanField("Destaque na Home", default=False)

    created_at = models.DateTimeField("Cadastrado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return f"{self.brand.name} {self.model} {self.year_manufacture}/{self.year_model}"

    @property
    def cover_photo(self):
        cover = self.photos.filter(is_cover=True).first()
        return cover or self.photos.first()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand.name}-{self.model}-{self.year_model}")
            slug = base_slug
            counter = 1
            while Vehicle.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class VehiclePhoto(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="Veículo",
    )
    image = models.ImageField("Foto", upload_to="vehicles/%Y/%m/")
    is_cover = models.BooleanField("Foto Principal (Capa)", default=False)
    order = models.PositiveSmallIntegerField("Ordem", default=0)

    class Meta:
        verbose_name = "Foto do Veículo"
        verbose_name_plural = "Fotos do Veículo"
        ordering = ["-is_cover", "order", "id"]

    def __str__(self):
        return f"Foto de {self.vehicle}"


class Lead(models.Model):
    class IntentChoices(models.TextChoices):
        INTEREST = "interesse", "Tenho interesse neste veículo"
        FINANCING = "financiamento", "Quero simular financiamento"
        TRADE_IN = "troca", "Quero dar meu usado na troca"
        VISIT = "visita", "Quero agendar uma visita"

    class StatusChoices(models.TextChoices):
        NEW = "novo", "Novo"
        CONTACTED = "em_contato", "Em contato"
        CLOSED = "fechado", "Venda concluída"
        LOST = "perdido", "Não avançou"

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="leads",
        verbose_name="Veículo",
    )
    name = models.CharField("Nome do Cliente", max_length=100)
    phone = models.CharField("WhatsApp / Telefone", max_length=25)
    intent = models.CharField(
        "Assunto",
        max_length=20,
        choices=IntentChoices.choices,
        default=IntentChoices.INTEREST,
    )
    status = models.CharField(
        "Status do Atendimento",
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW,
    )
    notes = models.TextField("Observações internas", blank=True)
    created_at = models.DateTimeField("Recebido em", auto_now_add=True)

    class Meta:
        verbose_name = "Interessado (Lead)"
        verbose_name_plural = "Interessados (Leads)"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.vehicle}"