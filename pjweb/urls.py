from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from newletters.views import HomeView, NewslettersView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^newsletter/$', NewslettersView.as_view(), name="newsletters"),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^jobs/', include('job.urls')),
    url(r'^developers/', include('accounts.urls')),
    url(r'^companies/', include('companys.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
