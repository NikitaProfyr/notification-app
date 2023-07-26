from datetime import datetime
import logging
import pytz

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView
from notification.forms import MailListForm, ClientForm
from notification.models import MailingListModel, ClientModel, MassageModel
from notification.servieces import sendMassage, filterClients

# Create your views here.

log = logging.getLogger(__name__)


class HomePage(TemplateView):
    """Главная страница"""
    template_name = 'notification/index.html'
    log.info('Открыта главная страница')


class MailingListView(ListView):
    """Страница отображения списка рассылок"""
    model = MailingListModel
    template_name = 'notification/mailing-list-view.html'
    context_object_name = 'MailingLists'
    log.info('Открыта страница оо списком рассылок')


class MailingListDetailView(DetailView):
    """Страница отображения деталей рассылки"""
    template_name = 'notification/mailing-detail-view.html'
    model = MailingListModel
    context_object_name = 'MailingList'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        log.info(f'Открыта страница с детальным описанием рассылки #{context["MailingList"].pk}')
        massages = MassageModel.objects.prefetch_related('Client').filter(MailingList=context['MailingList'].pk)
        for massage in massages:
            log.info(f'     пользователь, получивший рассылку:{massage.Client.numberPhone}')
        context.update({
            'massages': massages,
        })
        return context


class MailingListCreateView(CreateView):
    """Страница создания рассылки"""
    model = MailingListModel
    form_class = MailListForm
    template_name = 'notification/mailing-create-view.html'
    success_url = reverse_lazy('Mailing')
    log.info(f'Открыта страница для созданием рассылки')

    def form_valid(self, form):
        utc = pytz.UTC
        success_url = self.get_success_url()
        responseData = form.cleaned_data
        clients = filterClients(responseData['filterClientCodeOperator'], responseData['filterClientTag'])
        if responseData['dateFinish'] <= utc.localize(datetime.now()):
            self.errorMassage = 'дата окончания рассылки должна быть больше текущего времени'
            log.info(
                f'-----Дата окончания рассылки должна быть больше текущего времени: текущие дата и время: {utc.localize(datetime.now())}, дата окончания: {responseData["dateFinish"]}')
            return render(self.request, self.template_name, {'errorMassage': self.errorMassage, 'form': form})
        else:
            if not clients:
                self.errorMassage = 'выбранные клиенты отсутствуют'
                log.info(f'-----Выбранные клиенты отсутствуют')
                return render(self.request, self.template_name, {'errorMassage': self.errorMassage, 'form': form})
            else:
                MailingListModel.objects.create(textMassage=responseData['textMassage'],
                                                filterClientCodeOperator=responseData['filterClientCodeOperator'],
                                                filterClientTag=responseData['filterClientTag'],
                                                dateFinish=responseData['dateFinish'])
                lastMailingList = MailingListModel.objects.all().last()
                log.info(f'     Создана рассылка №{lastMailingList.pk}')
                sendMassage(clients, lastMailingList)
                log.info(f'     Рассылка завершена №{lastMailingList.pk}')
                return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return self.success_url


class MailingListDeleteView(DeleteView):
    """Страница удаления рассылки"""
    model = MailingListModel
    success_url = reverse_lazy('Mailing')
    template_name = 'notification/mailing-delete-view.html'
    context_object_name = 'MailingList'


class ClientListView(ListView):
    """Страница отображения списка клиентов"""
    model = ClientModel
    template_name = 'notification/client-list-view.html'
    context_object_name = 'Clients'


class ClientCreateView(CreateView):
    """Страница создания клиента"""
    model = ClientModel
    form_class = ClientForm
    template_name = 'notification/client-create-view.html'
    success_url = reverse_lazy('Clients')


class ClientDetailView(DetailView):
    """Страница отображения деталей клиента"""
    template_name = 'notification/client-detail-view.html'
    model = ClientModel
    context_object_name = 'Client'


class ClientDeleteView(DeleteView):
    """Страница удаления клиента"""
    model = ClientModel
    success_url = reverse_lazy('Clients')
    template_name = 'notification/client-delete-view.html'
    context_object_name = 'Client'
