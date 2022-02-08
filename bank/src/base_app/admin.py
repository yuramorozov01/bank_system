from base_app.models import BankSettings
from django.contrib import admin

admin.site.register(BankSettings)

bank_settings, created = BankSettings.objects.get_or_create()
