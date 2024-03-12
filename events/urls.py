from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="Events API",
    ),
    public=True,
)
static_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
media_urls = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("main/", include("main.urls")),
    path("chat/", include("chat.urls")),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0)),
]

if settings.DEBUG:
    urlpatterns += static_urls + media_urls
