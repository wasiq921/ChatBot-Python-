from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_index, name="render_index"),
    path('<str:name>/', views.render_chat_room, name="render_chat_room"),
]
