from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('Pharmacy-Agent/' , PharmacyAgent.as_view(), name="Pharmacy-Agent"),
    path('upload/', Upload.as_view(), name='upload'),
    path('chat-session/' , Creation.as_view(), name="chat_ession")
]