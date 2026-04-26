from django.urls import path

from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.InfoView.as_view(), name='info'),

    # Меню
    path('menu/', views.MenuView.as_view(), name='index'),
]
