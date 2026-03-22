from django.db import models

AVAILABLE = "available"
IN_USE = "in_use"
UNDER_REPAIR = "under_repair"
RETIRED = "retired"

STATUS_CHOICES = [
    (AVAILABLE, "Available"),
    (IN_USE, "In Use"),
    (UNDER_REPAIR, "Under Repair"),
    (RETIRED, "Retired"),
]


class Ward(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Cushion(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    purchase_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)
    ward = models.ForeignKey(
        Ward, null=True, blank=True, on_delete=models.SET_NULL, related_name="cushions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.serial_number})"

    @property
    def asset_type(self):
        return "cushion"

    class Meta:
        ordering = ["-created_at"]


class Wheelchair(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    purchase_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)
    ward = models.ForeignKey(
        Ward, null=True, blank=True, on_delete=models.SET_NULL, related_name="wheelchairs"
    )
    paired_cushion = models.OneToOneField(
        Cushion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="wheelchair",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.serial_number})"

    @property
    def asset_type(self):
        return "wheelchair"

    class Meta:
        ordering = ["-created_at"]
