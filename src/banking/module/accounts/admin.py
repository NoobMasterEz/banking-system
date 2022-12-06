from django.contrib import admin

from .models import AccountInformation, AccountStatement


@admin.register(AccountInformation)
class AccountInformationAdmin(admin.ModelAdmin):
    pass


@admin.register(AccountStatement)
class AccountStatementAdmin(admin.ModelAdmin):
    readonly_fields = ['guid']
