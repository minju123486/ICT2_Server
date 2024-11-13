"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AR_DATA import views
urlpatterns = [
    path('', views.index),
    path('upload_image/', views.upload_image),
    path('trasmit_image/', views.transmit_image),
    path('stamp_data/', views.stamp_data),
    path('mock_stamp_data/', views.mock_stamp_data),
    path('LLM_QUEST/', views.LLM_QUEST)
]
