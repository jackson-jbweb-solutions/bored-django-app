from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .forms import CushionForm, WardForm, WheelchairForm
from .models import STATUS_CHOICES, Cushion, Ward, Wheelchair


# ── Ward views ────────────────────────────────────────────────────────────────

@login_required
def ward_list(request):
    wards = Ward.objects.all()
    return render(request, "assets/ward_list.html", {"wards": wards})


@login_required
def ward_create(request):
    if request.method == "POST":
        form = WardForm(request.POST)
        if form.is_valid():
            ward = form.save()
            return render(request, "assets/ward_create_success.html", {"ward": ward})
    else:
        form = WardForm()
    return render(request, "assets/ward_form.html", {"form": form})


@login_required
def ward_edit(request, pk):
    ward = get_object_or_404(Ward, pk=pk)
    if request.method == "POST":
        form = WardForm(request.POST, instance=ward)
        if form.is_valid():
            ward = form.save()
            return render(request, "assets/ward_row.html", {"ward": ward})
    else:
        form = WardForm(instance=ward)
    return render(request, "assets/ward_edit_row.html", {"form": form, "ward": ward})


@login_required
def ward_row(request, pk):
    ward = get_object_or_404(Ward, pk=pk)
    return render(request, "assets/ward_row.html", {"ward": ward})


@login_required
@require_http_methods(["DELETE"])
def ward_delete(request, pk):
    ward = get_object_or_404(Ward, pk=pk)
    ward.delete()
    return HttpResponse("")  # pyright: ignore[reportArgumentType]


# ── Asset list views ──────────────────────────────────────────────────────────

@login_required
def asset_list(request):
    wards = Ward.objects.all()
    wheelchairs = Wheelchair.objects.select_related("ward", "paired_cushion").all()
    cushions = Cushion.objects.select_related("ward", "wheelchair").all()
    assets = sorted(
        list(wheelchairs) + list(cushions),
        key=lambda x: x.created_at,
        reverse=True,
    )
    return render(request, "assets/asset_list.html", {
        "assets": assets,
        "wards": wards,
        "status_choices": STATUS_CHOICES,
    })


@login_required
def asset_list_rows(request):
    type_filter = request.GET.get("type")
    ward_filter = request.GET.get("ward")
    status_filter = request.GET.get("status")

    wheelchairs = []
    cushions = []

    if type_filter != "cushion":
        qs = Wheelchair.objects.select_related("ward", "paired_cushion").all()
        if ward_filter:
            qs = qs.filter(ward_id=ward_filter)
        if status_filter:
            qs = qs.filter(status=status_filter)
        wheelchairs = list(qs)

    if type_filter != "wheelchair":
        qs = Cushion.objects.select_related("ward", "wheelchair").all()
        if ward_filter:
            qs = qs.filter(ward_id=ward_filter)
        if status_filter:
            qs = qs.filter(status=status_filter)
        cushions = list(qs)

    assets = sorted(wheelchairs + cushions, key=lambda x: x.created_at, reverse=True)
    return render(request, "assets/asset_list_rows.html", {"assets": assets})


@login_required
def asset_create_form(request):
    asset_type = request.GET.get("type", "wheelchair")
    if asset_type == "cushion":
        form = CushionForm()
    else:
        asset_type = "wheelchair"
        form = WheelchairForm()
    return render(request, "assets/asset_create_form.html", {"form": form, "type": asset_type})


# ── Wheelchair views ──────────────────────────────────────────────────────────

@login_required
def wheelchair_create(request):
    form = WheelchairForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        wc = form.save()
        return render(request, "assets/wheelchair_create_success.html", {"wc": wc})
    response = render(request, "assets/asset_create_form.html", {"form": form, "type": "wheelchair"})
    if request.method == "POST":
        # On invalid POST: retarget to form container so errors display correctly
        response["HX-Retarget"] = "#asset-form-container"
        response["HX-Reswap"] = "innerHTML"
    return response


@login_required
def wheelchair_edit(request, pk):
    wc = get_object_or_404(Wheelchair, pk=pk)
    if request.method == "POST":
        form = WheelchairForm(request.POST, instance=wc)
        if form.is_valid():
            wc = form.save()
            return render(request, "assets/wheelchair_row.html", {"wc": wc})
    else:
        form = WheelchairForm(instance=wc)
    return render(request, "assets/wheelchair_edit_row.html", {"form": form, "wc": wc})


@login_required
def wheelchair_row(request, pk):
    wc = get_object_or_404(Wheelchair, pk=pk)
    return render(request, "assets/wheelchair_row.html", {"wc": wc})


@login_required
@require_http_methods(["DELETE"])
def wheelchair_delete(request, pk):
    wc = get_object_or_404(Wheelchair, pk=pk)
    wc.delete()
    return HttpResponse("")  # pyright: ignore[reportArgumentType]


# ── Cushion views ─────────────────────────────────────────────────────────────

@login_required
def cushion_create(request):
    form = CushionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        cushion = form.save()
        return render(request, "assets/cushion_create_success.html", {"cushion": cushion})
    response = render(request, "assets/asset_create_form.html", {"form": form, "type": "cushion"})
    if request.method == "POST":
        response["HX-Retarget"] = "#asset-form-container"
        response["HX-Reswap"] = "innerHTML"
    return response


@login_required
def cushion_edit(request, pk):
    cushion = get_object_or_404(Cushion, pk=pk)
    if request.method == "POST":
        form = CushionForm(request.POST, instance=cushion)
        if form.is_valid():
            cushion = form.save()
            return render(request, "assets/cushion_row.html", {"cushion": cushion})
    else:
        form = CushionForm(instance=cushion)
    return render(request, "assets/cushion_edit_row.html", {"form": form, "cushion": cushion})


@login_required
def cushion_row(request, pk):
    cushion = get_object_or_404(Cushion, pk=pk)
    return render(request, "assets/cushion_row.html", {"cushion": cushion})


@login_required
@require_http_methods(["DELETE"])
def cushion_delete(request, pk):
    cushion = get_object_or_404(Cushion, pk=pk)
    cushion.delete()
    return HttpResponse("")  # pyright: ignore[reportArgumentType]
