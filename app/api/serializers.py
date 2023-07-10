from rest_framework.serializers import ModelSerializer

from notification.models import ClientModel, MailingListModel, MassageModel



class MassageSerializer(ModelSerializer):
    class Meta:
        model = MassageModel
        fields = '__all__'


class ClientsSerializer(ModelSerializer):
    class Meta:
        model = ClientModel
        fields = '__all__'


class MailingListSerializer(ModelSerializer):
    class Meta:
        model = MailingListModel
        fields = '__all__'
