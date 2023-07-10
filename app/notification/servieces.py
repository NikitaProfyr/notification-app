"""Здесь находятся вспомогательные функции и классы для реализации API"""
import logging
import requests
from notification.models import MassageModel, ClientModel

log = logging.getLogger(__name__)


class OpenAPIConnection:
    """Класс для реализации подключения к внешнему API"""

    def __init__(self, url, jsonData):
        self.url = url
        self.jsonData = jsonData
        self.headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjAyODAxMjcsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IlNjaG5laWRlciBOaWtpdNCwIn0.z-bsUXruyg6ByLgQgf_sUp7q6AlPDsiNI-2dE8Qtfvg'
        }
        log.info("     Отправлен запрос на внешний API")
        log.info(f"         Отправляемые данные{self.jsonData}")
        self.response = requests.post(url=self.url, json=self.jsonData, headers=self.headers)
        log.info(f"         Ответ с сервера{self.get_jsonResponse()}")

    def get_response(self):
        return self.response

    def get_jsonResponse(self):
        return self.response.json()


def sendMassage(allClients, lastMailingList):
    """
    Функция для рассылки сообщений
    allClients: список клиентов
    lastMailingList: новая созданная рассылка
    """
    for client in allClients:
        MassageModel.objects.create(status='доставлено', MailingList=lastMailingList, Client=client)
        log.info(f"         Сообщение доставлену клиенту №{client.numberPhone}")
        lastMassage = MassageModel.objects.all().last()
        url = f"https://probe.fbrq.cloud/v1/send/{lastMassage.pk}"
        dataResponseAPIConnection = {
            'id': lastMassage.pk,
            "phone": client.numberPhone,
            "text": lastMailingList.textMassage,
        }
        objConnection = OpenAPIConnection(url, dataResponseAPIConnection)



def filterClients(filterCodeOperator, filterTag):
    """Функция для фильтрации клиентов по тгу и коду оператора"""
    if filterCodeOperator == '':
        filterCodeOperator = None
    if filterTag == '':
        filterTag = None
    if filterCodeOperator and filterTag:
        clients = ClientModel.objects.filter(
            codeOperator=filterCodeOperator,
            tag=filterTag).all()
    elif not filterTag or not filterCodeOperator:
        if filterTag:
            clients = ClientModel.objects.filter(tag=filterTag).all()
        else:
            clients = ClientModel.objects.filter(codeOperator=filterCodeOperator).all()
    if not filterCodeOperator and not filterTag:
        clients = ClientModel.objects.all()
    return clients
