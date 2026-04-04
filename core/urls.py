from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index.html', views.home, name='index'),
    path('set-currency/', views.set_currency, name='set_currency'),
    path('speakers/', views.speakers, name='speakers'),
    path('programme/', views.programme, name='programme'),
    path('pricing/', views.pricing, name='pricing'),
    path('sponsors/', views.sponsors, name='sponsors'),
    path('register/', views.register, name='register'),
    path('register/success/<int:registration_id>/', views.registration_success, name='registration_success'),
    path('offers/', views.offers, name='offers'),
    path('offers/playbook/', views.capture_playbook_lead, name='capture_playbook_lead'),
    path('track-click/', views.track_click, name='track_click'),
    path('dashboard/registrations/', views.registration_dashboard, name='registration_dashboard'),
]
