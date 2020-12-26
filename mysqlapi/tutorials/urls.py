from django.conf.urls import url
from tutorials import views

urlpatterns = [
    url(r"^api/tutorials$", views.tutorials_list),
    url(r"^api/tutorials/(?P<pk>[0-9]+)$", views.tutorial_details),
    url(r"^api/tutorials/published$", views.tutorials_list_published),
]