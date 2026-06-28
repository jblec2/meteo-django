# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class EnvcaWeatherInventory(models.Model):
    name = models.CharField(db_column='Name', max_length=60, blank=True, null=True)  # Field name made lowercase.
    province = models.CharField(db_column='Province', max_length=25, blank=True, null=True)  # Field name made lowercase.
    climate_id = models.CharField(db_column='Climate ID', unique=True, max_length=12, blank=True, null=False, primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    station_id = models.IntegerField(db_column='Station ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    wmo_id = models.IntegerField(db_column='WMO ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tc_id = models.CharField(db_column='TC ID', max_length=12, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    latitude_decimal_degrees_field = models.FloatField(db_column='Latitude (Decimal Degrees)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    longitude_decimal_degrees_field = models.FloatField(db_column='Longitude (Decimal Degrees)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    elevation_m_field = models.FloatField(db_column='Elevation (m)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    first_year = models.IntegerField(db_column='First Year', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_year = models.IntegerField(db_column='Last Year', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hly_first_year = models.IntegerField(db_column='HLY First Year', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hly_last_year = models.IntegerField(db_column='HLY Last Year', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dly_first_year = models.IntegerField(db_column='DLY First Year', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dly_last_year = models.IntegerField(db_column='DLY Last Year', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mly_first_year = models.IntegerField(db_column='MLY First Year', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mly_last_year = models.IntegerField(db_column='MLY Last Year', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'envca_weather_inventory'