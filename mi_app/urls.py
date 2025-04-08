

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('header_data/', views.header_data, name='header_data'),
    path('header/create/', views.header_create, name='header_create'),
    path('detail/upload/', views.detail_upload, name='detail_upload'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/data/', views.dashboard_data, name='dashboard_data'),
]

