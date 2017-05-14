from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
# from django.contrib import admin


from .views import (
    AccountListView, AccountDetailView, AccountUpdateView, AccountDeleteView
)

urlpatterns = [
    url(r'^$', AccountListView.as_view(), name='accounts'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)/$',
        AccountDetailView.as_view(), name='detail_accounts'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)/edit/$',
        AccountUpdateView.as_view(), name='update_accounts'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)/delete/$',
        AccountDeleteView.as_view(), name='delete_accounts'),
]
