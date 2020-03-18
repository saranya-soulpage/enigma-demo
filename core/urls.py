"""enigma URL Configuration

"""

from django.urls import path
from django.views.generic import TemplateView


from django.conf import settings
from django.conf.urls import include, url
from .views import ReposRequest, repo_info_view

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html')),
    path("accounts/profile/", TemplateView.as_view(template_name="profile.html")),
    path("", ReposRequest.as_view(), name="repos_requesting"),
    path("repo_info/<repo_name>/", repo_info_view, name="repo_name"),
]
