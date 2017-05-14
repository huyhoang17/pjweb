from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
# from django.contrib import admin


from .views import JobListView, JobDetailView, JobCreateView, JobDeleteView

urlpatterns = [
    url(r'^$', JobListView.as_view(), name='jobs'),
    # url(r'^(?P<pk>\d+)/$', JobDetailView.as_view(), name='detail_jobs'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)/$',
        JobDetailView.as_view(), name='detail_jobs'),
    url(r'^create/$', JobCreateView.as_view(), name='create_jobs'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w.@+-]+)/delete/$',
        JobDeleteView.as_view(), name='delete_jobs'),
]
