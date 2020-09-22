from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views
from . import ajax_datatable_views

app_name = 'frontend'


urlpatterns = [
    path('', TemplateView.as_view(template_name="frontend/index.html"), name="index"),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGIN_REDIRECT_URL), name='logout'),

    path('tracks/', views.tracks_list_view, name="tracks-list"),
    path('ajax_datatable/tracks/', ajax_datatable_views.TrackAjaxDatatableView.as_view(), name="ajax_datatable_track"),
]
