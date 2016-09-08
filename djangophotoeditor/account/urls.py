from account import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url('', include('social.apps.django_app.urls', namespace='social')),
]