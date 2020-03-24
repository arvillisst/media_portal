from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('portal.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)