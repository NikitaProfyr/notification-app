from django.contrib import admin

from notification.models import MailingListModel, ClientModel, MassageModel


# Register your models here.
@admin.register(MailingListModel)
class MailingListModelAdmin(admin.ModelAdmin):
    model = MailingListModel

@admin.register(ClientModel)
class ClientModelAdmin(admin.ModelAdmin):
    model = ClientModel

@admin.register(MassageModel)
class MassageModelAdmin(admin.ModelAdmin):
    model = MassageModel
