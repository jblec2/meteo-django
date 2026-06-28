from django.shortcuts import render
import datetime
import io
import zipfile
import requests
from pandas import date_range
from django.http import HttpResponse
from django.urls import reverse
from .models import EnvcaWeatherInventory
from .utils import TIMEFRAME_MAPPING, build_bulk_data_url
from django.views import generic


class MapView(generic.ListView):
    model = EnvcaWeatherInventory
    template_name="dashboard/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stations = context["object_list"]
        context["stations_json"] = [
            {
                "name": station.name,
                "province": station.province,
                "latitude": station.latitude_decimal_degrees_field,
                "longitude": station.longitude_decimal_degrees_field,
                "climate_id": station.climate_id,
                "station_id": station.station_id,
                "download_url": reverse("dashboard:download_station", args=[station.pk]),
                "elevation_m": station.elevation_m_field,
                "first_year": station.first_year,
                "last_year": station.last_year,
                "hly_first_year": station.hly_first_year,
                "hly_last_year": station.hly_last_year,
                "dly_first_year": station.dly_first_year,
                "dly_last_year": station.dly_last_year,
                "mly_first_year": station.mly_first_year,
                "mly_last_year": station.mly_last_year
            }
            for station in stations
            if station.latitude_decimal_degrees_field is not None
            and station.longitude_decimal_degrees_field is not None
        ]
        context["amount"] = len(stations)
        return context

class DownloadView(generic.DetailView):
    model = EnvcaWeatherInventory
    template_name = "dashboard/station_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        error = None
        if {"date_beginning", "date_end", "freq"} <= set(request.GET):
            error = self._validate(request.GET)
            if error is None:
                try:
                    return self._download(request.GET)
                except requests.RequestException:
                    error = "Could not retrieve data from Environment Canada. Please try again later."
        context = self.get_context_data(object=self.object, error=error)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station = self.object
        available_freqs = {
            "hourly": bool(station.hly_first_year and station.hly_last_year),
            "daily": bool(station.dly_first_year and station.dly_last_year),
            "monthly": bool(station.mly_first_year and station.mly_last_year),
        }
        context["available_freqs"] = available_freqs
        context["default_freq"] = next((freq for freq in ("hourly", "daily", "monthly") if available_freqs[freq]), None)
        return context

    def _validate(self, params):
        if not self.object.station_id:
            return "This station has no Station ID on file; data cannot be downloaded."
        if params.get("freq") not in TIMEFRAME_MAPPING:
            return "Please choose a valid data frequency."
        try:
            date_begin = datetime.date.fromisoformat(params["date_beginning"])
            date_end = datetime.date.fromisoformat(params["date_end"])
        except ValueError:
            return "Please enter valid dates."
        if date_begin > date_end:
            return "The beginning date must be before the end date."
        return None

    def _download(self, params):
        station = self.object
        freq = params["freq"]
        date_begin = datetime.date.fromisoformat(params["date_beginning"])
        date_end = datetime.date.fromisoformat(params["date_end"])

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for month_start in date_range(start=date_begin.replace(day=1), end=date_end, freq="MS"):
                url = build_bulk_data_url(station.station_id, month_start.year, month_start.month, freq)
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                filename = f"{station.name}_{station.station_id}_{month_start.year}_{month_start.month:02d}.csv"
                zf.writestr(filename, response.content)

        response = HttpResponse(buffer.getvalue(), content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{station.name}_{station.station_id}_{freq}.zip"'
        return response