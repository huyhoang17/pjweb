from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
# from django.contrib import admin


from .views import (
    CompanyListView, CompanyDetailView, CompanyCreateView
)

urlpatterns = [
    url(r'^$', CompanyListView.as_view(), name='companies'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)/$',
        CompanyDetailView.as_view(), name='detail_companys'),
    url(r'^create/$', CompanyCreateView.as_view(), name='create_companies'),
]
