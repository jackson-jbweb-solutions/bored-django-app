from django.db import IntegrityError
from django.test import TestCase

from .models import AVAILABLE, Cushion, Ward, Wheelchair


class WardModelTest(TestCase):
    def test_str_returns_name(self):
        ward = Ward(name="Ward A")
        self.assertEqual(str(ward), "Ward A")

    def test_name_is_unique(self):
        Ward.objects.create(name="Ward A")
        with self.assertRaises(IntegrityError):
            Ward.objects.create(name="Ward A")


class CushionModelTest(TestCase):
    def setUp(self):
        self.ward = Ward.objects.create(name="Ward A")

    def test_str_includes_make_model_serial(self):
        cushion = Cushion(make="Roho", model="Quadtro", serial_number="C001")
        self.assertIn("Roho", str(cushion))
        self.assertIn("C001", str(cushion))

    def test_default_status_is_available(self):
        cushion = Cushion.objects.create(
            serial_number="C001", make="Roho", model="Quadtro"
        )
        self.assertEqual(cushion.status, AVAILABLE)

    def test_serial_number_is_unique(self):
        Cushion.objects.create(serial_number="C001", make="Roho", model="Quadtro")
        with self.assertRaises(IntegrityError):
            Cushion.objects.create(serial_number="C001", make="Other", model="Other")

    def test_ward_can_be_null(self):
        cushion = Cushion.objects.create(
            serial_number="C002", make="Roho", model="Quadtro"
        )
        self.assertIsNone(cushion.ward)

    def test_asset_type_is_cushion(self):
        cushion = Cushion(make="Roho", model="Quadtro", serial_number="C001")
        self.assertEqual(cushion.asset_type, "cushion")


class WheelchairModelTest(TestCase):
    def setUp(self):
        self.cushion = Cushion.objects.create(
            serial_number="C001", make="Roho", model="Quadtro"
        )

    def test_str_includes_make_model_serial(self):
        wc = Wheelchair(make="Karma", model="Ergo", serial_number="W001")
        self.assertIn("Karma", str(wc))
        self.assertIn("W001", str(wc))

    def test_paired_cushion_can_be_null(self):
        wc = Wheelchair.objects.create(
            serial_number="W001", make="Karma", model="Ergo"
        )
        self.assertIsNone(wc.paired_cushion)

    def test_cushion_can_only_be_paired_with_one_wheelchair(self):
        Wheelchair.objects.create(
            serial_number="W001", make="Karma", model="Ergo",
            paired_cushion=self.cushion
        )
        with self.assertRaises(IntegrityError):
            Wheelchair.objects.create(
                serial_number="W002", make="Karma", model="Ergo",
                paired_cushion=self.cushion
            )

    def test_asset_type_is_wheelchair(self):
        wc = Wheelchair(make="Karma", model="Ergo", serial_number="W001")
        self.assertEqual(wc.asset_type, "wheelchair")


from django.contrib.auth import get_user_model

from .forms import CushionForm, WardForm, WheelchairForm


class WheelchairFormTest(TestCase):
    def setUp(self):
        self.unpaired_cushion = Cushion.objects.create(
            serial_number="C001", make="Roho", model="Quadtro"
        )
        self.other_wc = Wheelchair.objects.create(
            serial_number="W001", make="Karma", model="Ergo"
        )
        self.paired_cushion = Cushion.objects.create(
            serial_number="C002", make="Roho", model="High"
        )
        self.other_wc.paired_cushion = self.paired_cushion
        self.other_wc.save()

    def test_create_form_shows_only_unpaired_cushions(self):
        form = WheelchairForm()
        qs = form.fields["paired_cushion"].queryset
        self.assertIn(self.unpaired_cushion, qs)
        self.assertNotIn(self.paired_cushion, qs)

    def test_edit_form_includes_already_paired_cushion(self):
        form = WheelchairForm(instance=self.other_wc)
        qs = form.fields["paired_cushion"].queryset
        # The currently-paired cushion must appear
        self.assertIn(self.paired_cushion, qs)
        # Unpaired cushions must also appear (user can swap to them)
        self.assertIn(self.unpaired_cushion, qs)


User = get_user_model()


class ViewAccessTest(TestCase):
    """All asset views redirect to login when unauthenticated."""

    def test_asset_list_requires_login(self):
        response = self.client.get("/assets/")
        self.assertRedirects(response, "/accounts/login/?next=/assets/")

    def test_ward_list_requires_login(self):
        response = self.client.get("/assets/wards/")
        self.assertRedirects(response, "/accounts/login/?next=/assets/wards/")


class WardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
        self.client.login(username="u", password="p")

    def test_ward_list_returns_200(self):
        response = self.client.get("/assets/wards/")
        self.assertEqual(response.status_code, 200)

    def test_ward_create_valid(self):
        response = self.client.post("/assets/wards/create/", {"name": "ICU"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Ward.objects.filter(name="ICU").exists())

    def test_ward_create_invalid_missing_name(self):
        response = self.client.post("/assets/wards/create/", {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ward.objects.count(), 0)

    def test_ward_delete(self):
        ward = Ward.objects.create(name="ICU")
        response = self.client.delete(f"/assets/wards/{ward.pk}/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Ward.objects.filter(pk=ward.pk).exists())

    def test_ward_edit_valid(self):
        ward = Ward.objects.create(name="ICU")
        response = self.client.post(f"/assets/wards/{ward.pk}/edit/", {"name": "HDU"})
        self.assertEqual(response.status_code, 200)
        ward.refresh_from_db()
        self.assertEqual(ward.name, "HDU")


class AssetListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
        self.client.login(username="u", password="p")

    def test_asset_list_returns_200(self):
        response = self.client.get("/assets/")
        self.assertEqual(response.status_code, 200)

    def test_asset_list_rows_filters_by_type(self):
        Wheelchair.objects.create(serial_number="W001", make="Karma", model="Ergo")
        Cushion.objects.create(serial_number="C001", make="Roho", model="Quadtro")
        response = self.client.get("/assets/rows/?type=wheelchair")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "W001")
        self.assertNotContains(response, "C001")

    def test_asset_list_rows_filters_by_status(self):
        Wheelchair.objects.create(serial_number="W001", make="K", model="E", status="retired")
        Wheelchair.objects.create(serial_number="W002", make="K", model="E", status="available")
        response = self.client.get("/assets/rows/?status=retired")
        self.assertContains(response, "W001")
        self.assertNotContains(response, "W002")

    def test_asset_list_rows_filters_by_ward(self):
        ward_a = Ward.objects.create(name="ICU")
        ward_b = Ward.objects.create(name="HDU")
        Wheelchair.objects.create(serial_number="W001", make="K", model="E", ward=ward_a)
        Wheelchair.objects.create(serial_number="W002", make="K", model="E", ward=ward_b)
        response = self.client.get(f"/assets/rows/?ward={ward_a.pk}")
        self.assertContains(response, "W001")
        self.assertNotContains(response, "W002")


class WheelchairViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
        self.client.login(username="u", password="p")

    def test_wheelchair_create_valid(self):
        response = self.client.post(
            "/assets/wheelchairs/create/",
            {"serial_number": "W001", "make": "Karma", "model": "Ergo",
             "status": "available", "ward": "", "paired_cushion": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Wheelchair.objects.filter(serial_number="W001").exists())

    def test_wheelchair_delete(self):
        wc = Wheelchair.objects.create(serial_number="W001", make="Karma", model="Ergo")
        response = self.client.delete(f"/assets/wheelchairs/{wc.pk}/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Wheelchair.objects.filter(pk=wc.pk).exists())

    def test_wheelchair_edit_valid(self):
        wc = Wheelchair.objects.create(serial_number="W001", make="Karma", model="Ergo")
        response = self.client.post(
            f"/assets/wheelchairs/{wc.pk}/edit/",
            {"serial_number": "W001", "make": "Quickie", "model": "Q50",
             "status": "available", "ward": "", "paired_cushion": ""},
        )
        self.assertEqual(response.status_code, 200)
        wc.refresh_from_db()
        self.assertEqual(wc.make, "Quickie")


class CushionViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
        self.client.login(username="u", password="p")

    def test_cushion_create_valid(self):
        response = self.client.post(
            "/assets/cushions/create/",
            {"serial_number": "C001", "make": "Roho", "model": "Quadtro",
             "status": "available", "ward": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Cushion.objects.filter(serial_number="C001").exists())

    def test_cushion_delete(self):
        cushion = Cushion.objects.create(serial_number="C001", make="Roho", model="Quadtro")
        response = self.client.delete(f"/assets/cushions/{cushion.pk}/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Cushion.objects.filter(pk=cushion.pk).exists())
