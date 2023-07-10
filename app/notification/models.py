from django.db import models


# Create your models here.


class MailingListModel(models.Model):
    """Модель Рассылки"""
    dateStart = models.DateTimeField(auto_now_add=True, verbose_name='дата и время запуска рассылки')
    textMassage = models.TextField(verbose_name='текст сообщения для доставки клиенту')
    filterClientCodeOperator = models.IntegerField(null=True, blank=True, max_length=11,
                                                   verbose_name='фильтр клиентов по коду оператора')
    filterClientTag = models.CharField(null=True, blank=True, max_length=50, verbose_name='фильтр клиентов по тэгу')
    dateFinish = models.DateTimeField(verbose_name='дата и время окончания рассылки')

    class Meta:
        verbose_name_plural = "рассылки"


class ClientModel(models.Model):
    """Модель Клиента"""
    numberPhone = models.IntegerField(max_length=11, verbose_name='номер телефона клиента')
    codeOperator = models.CharField(max_length=150, verbose_name='код мобильного оператора')
    tag = models.CharField(max_length=50, verbose_name='тег (произвольная метка)')
    timeZone = models.CharField(max_length=100, verbose_name='часовой пояс')

    class Meta:
        verbose_name_plural = "клиенты"

    def __str__(self):
        return f'{self.numberPhone}'


class MassageModel(models.Model):
    """Модель Сообщения"""
    dateCreate = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания (отправки)')
    status = models.CharField(max_length=50, verbose_name='статус отправки')
    MailingList = models.ForeignKey(MailingListModel, on_delete=models.CASCADE, verbose_name='id рассылки, в рамках которой было отправлено сообщение')
    Client = models.ForeignKey(ClientModel, on_delete=models.CASCADE, verbose_name='id клиента, которому отправили')

    class Meta:
        verbose_name_plural = "сообщения"
