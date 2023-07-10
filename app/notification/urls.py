from django.urls import path

from notification.views import HomePage, \
    MailingListView, MailingListCreateView, \
    MailingListDetailView, MailingListDeleteView, \
    ClientListView, ClientCreateView, \
    ClientDetailView, ClientDeleteView



# app_name = 'notification'

urlpatterns = [
    path('', HomePage.as_view(), name='HomePage'),
    #
    path('mailing/', MailingListView.as_view(), name='Mailing'),
    path('mailing/create/', MailingListCreateView.as_view(), name='MailingCreate'),
    path('mailing/detail/<int:pk>', MailingListDetailView.as_view(), name='MailingDetail'),
    path('mailing/detail/delete/<int:pk>', MailingListDeleteView.as_view(), name='MailingDelete'),
    #
    path('clients/', ClientListView.as_view(), name='Clients'),
    path('clients/create/', ClientCreateView.as_view(), name='ClientCreate'),
    path('clients/detail/<int:pk>', ClientDetailView.as_view(), name='ClientDetail'),
    path('clients/detail/delete/<int:pk>', ClientDeleteView.as_view(), name='ClientDelete'),
]
