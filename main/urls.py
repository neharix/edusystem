from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from .views import *

urlpatterns = [
    # OpenAPI Spectacular routes
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "redoc/",
        SpectacularRedocView.as_view(
            url_name="schema",
        ),
        name="redoc",
    ),
    # Includes
    path("v1/bmdu/", include("bmdu_api.urls")),
    path("v1/mmu/", include("mmu_api.urls")),
    # Special routes
    path("admin/", admin.site.urls),
    path("__devtools__/download-log/", download_log_file, name="download_log_file"),
    path("__devtools__/clear-log/", clear_log_file, name="clear_log_file"),
    path("__devtools__/dump-json-data/", dump_json_data_view, name="get_json_dump"),
    path("__devtools__/dump-sql-data/", dump_sql_data_view, name="get_sql_dump"),
]
