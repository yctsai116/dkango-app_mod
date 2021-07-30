from django.urls import path


from . import views

app_name = "singlepage"
urlpatterns = [
    path("", views.index, name="index"),
    path("api_configuration", views.api_data, name="api_configuration"),
    path("api_urls", views.api_details, name="api_urls"),
    path("api_response", views.api_response, name="api_response"),
    path("api-details/<int:id>", views.api_details, name="api_details"),
]