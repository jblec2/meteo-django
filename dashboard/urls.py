from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.MapView.as_view(), name="total_amount_of_station"),
    path("<str:pk>/", views.DownloadView.as_view(), name="download_station"),
]

