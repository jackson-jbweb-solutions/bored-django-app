from django.contrib import admin

from .models import Cushion, Ward, Wheelchair

admin.site.register(Ward)
admin.site.register(Cushion)
admin.site.register(Wheelchair)
