from django.urls import path

from api.api import ClientAPIView, MailingListCreateAPIView

app_name = 'api_app'

urlpatterns = [
    path('clients/', ClientAPIView.as_view(), name="APIClientsList"),
    path('mailing/', MailingListCreateAPIView.as_view(), name="APIMailingListCreate"),

]