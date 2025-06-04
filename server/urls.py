"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

from main.views import dev_tools, echo

i18n_paths = i18n_patterns(path("api/__devtools__/", dev_tools, name="dev_tools"))

urlpatterns = (
    [
        path("api/", include("main.urls")),
        path("", echo),
    ]
    + debug_toolbar_urls()
    + i18n_paths
)
