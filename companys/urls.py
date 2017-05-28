from django.conf.urls import url
# from django.contrib import admin


from .views import (
    CompanyListView,
    CompanyDetailView,
    CompanyCreateView,
    CompanyDeleteView,
    CompanyUpdateView
)

urlpatterns = [
    url(r'^$', CompanyListView.as_view(), name='companies'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)/$',
        CompanyDetailView.as_view(), name='detail_companys'),
    url(r'^create/$', CompanyCreateView.as_view(), name='create_companies'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)/edit/$',
        CompanyUpdateView.as_view(), name='update_companies'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)/delete/$',
        CompanyDeleteView.as_view(), name='delete_companys'),
]
