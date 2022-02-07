from django.contrib import admin

from base_app.models import BankSettings

admin.site.register(BankSettings)

bank_settings, created = BankSettings.objects.get_or_create()
