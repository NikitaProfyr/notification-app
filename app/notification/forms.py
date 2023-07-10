from django.forms import ModelForm

from notification.models import MailingListModel, ClientModel


class MailListForm(ModelForm):
    """Форма для создания рассылки"""
    class Meta:
        model = MailingListModel
        fields = '__all__'

class ClientForm(ModelForm):
    """Форма для добавления клиента"""
    class Meta:
        model = ClientModel
        fields = '__all__'