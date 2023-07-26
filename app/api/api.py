from datetime import datetime

from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response


from api.serializers import ClientsSerializer, MailingListSerializer
from notification.models import ClientModel, MailingListModel
from notification.servieces import filterClients, sendMassage


class ClientAPIView(ListCreateAPIView):
    """Создать и просмотреть клиентов"""
    queryset = ClientModel.objects.all()
    serializer_class = ClientsSerializer


class MailingListCreateAPIView(ListCreateAPIView):
    """Создать и просмотреть рассылки"""
    queryset = MailingListModel.objects.all()
    serializer_class = MailingListSerializer

    def post(self, request, **kwargs):
        responseData = self.request.data
        clients = filterClients(responseData['filterClientCodeOperator'], responseData['filterClientTag'])
        if responseData['filterClientCodeOperator'] == '':
            filterClientCodeOperator = None
        else:
            filterClientCodeOperator = responseData['filterClientCodeOperator']
        dateFinish = datetime.strptime(responseData['dateFinish'],  '%Y-%m-%dT%H:%M')
        if dateFinish <= datetime.now().replace(tzinfo=None):
            errorMassage = 'дата окончания рассылки должна быть больше текущего времени'
            return Response(errorMassage)
        else:
            if not clients:
                errorMassage = 'выбранные клиенты отсутствуют'
                return Response(errorMassage)
            else:
                MailingListModel.objects.create(textMassage=responseData['textMassage'],
                                                filterClientCodeOperator=filterClientCodeOperator,
                                                filterClientTag=responseData['filterClientTag'],
                                                dateFinish=dateFinish)
                lastMailingList = MailingListModel.objects.all().last()
                sendMassage(clients, lastMailingList)
                return Response(200)
