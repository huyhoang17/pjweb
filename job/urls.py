from django.conf.urls import url

from .views import (
    JobListView,
    JobDetailView,
    JobCreateView,
    JobDeleteView,
    JobUpdateView
)

urlpatterns = [
    url(r'^$', JobListView.as_view(), name='jobs'),
    # url(r'^(?P<pk>\d+)/$', JobDetailView.as_view(), name='detail_jobs'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)/$',
        JobDetailView.as_view(), name='detail_jobs'),
    url(r'^create/$', JobCreateView.as_view(), name='create_jobs'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)/edit/$',
        JobUpdateView.as_view(), name='update_jobs'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)/delete/$',
        JobDeleteView.as_view(), name='delete_jobs'),
]
