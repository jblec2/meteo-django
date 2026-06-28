import argparse
from pathlib import Path
import requests
from pandas import read_csv, date_range, DataFrame
from datetime import date
from functools import lru_cache


TIMEFRAME_MAPPING = {"hourly": "1", "daily": "2", "monthly": "3"}


def build_bulk_data_url(station_id : str | int, year : int, month : int, freq : str, day : int = 14) -> str:
    return rf"https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={station_id}&Year={year}&Month={month}&Day={day}&timeframe={TIMEFRAME_MAPPING[freq]}&submit=Download+Data"

