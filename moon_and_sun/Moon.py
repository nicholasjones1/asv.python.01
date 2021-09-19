import argparse
import datetime
from calendar import timegm
from time import localtime, gmtime, mktime


import astropy
import pytz
from astroplan import Observer
from astroplan import moon_illumination
from astropy.coordinates import get_moon
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
import astropy.units as u

class Moon:
    def __init__(self, time_zone, latitude, longitude):
        self.timeZone = time_zone
        self.latitude = latitude
        self.longitude = longitude

    def get_ra_dec(self, utc_date_time):
        utc_date_time_str = utc_date_time.strftime("%Y-%m-%d %H:%M:%S")
        time = Time(utc_date_time_str, format='iso', scale='utc', out_subfmt='date*')
        moon_sky_coord = get_moon(time)
        print(str(round(moon_sky_coord.ra.deg, 6)))
        print(str(round(moon_sky_coord.dec.deg, 6)))


    def get_moon_illumination(self, utc_date_time):
        utc_date_time_str = utc_date_time.strftime("%Y-%m-%d %H:%M:%S")
        time = Time(utc_date_time_str, format='iso', scale='utc', out_subfmt='date*')
        print(str(round(moon_illumination(time), 2)))

    def get_moon_altaz(self, utc_date_time):
        observer = self.get_observer()
        zoned_time = self.get_zoned_time(utc_date_time)
        moonAltAz = observer.moon_altaz(zoned_time)
        print(str(round(moonAltAz.alt.deg, 2)))
        print(str(round(moonAltAz.az.deg, 2)))

    def get_next_rise(self, utc_date_time):
        observer = self.get_observer()
        zoned_time = self.get_zoned_time(utc_date_time)
        rise_time = observer.moon_rise_time(zoned_time, 'next')
        rise_datetime = rise_time.to_datetime()
        print(str(rise_datetime))
        return rise_time

    def get_nearest_rise(self, utc_date_time):
        observer = self.get_observer()
        zoned_time = self.get_zoned_time(utc_date_time)
        return observer.moon_rise_time(zoned_time, 'nearest')

    def get_previous_moon_rise(self, utc_date_time):
        observer = self.get_observer()
        zoned_time = self.get_zoned_time(utc_date_time)
        return observer.moon_rise_time(zoned_time, 'previous')

    def get_next_set(self, utc_date_time):
        observer = self.get_observer()
        zoned_time = self.get_zoned_time(utc_date_time)
        return observer.moon_set_time(zoned_time, 'next')

    def get_nearest_set(self, utc_date_time):
        observer = self.get_observer()
        zoned_time = self.get_zoned_time(utc_date_time)
        set_time =  observer.moon_set_time(zoned_time, 'nearest')
        print(str(set_time))
        return set_time

    def get_previous_set(self, utc_date_time):
        observer = self.get_observer()
        zoned_time = self.get_zoned_time(utc_date_time)
        return observer.moon_set_time(zoned_time, 'previous')

    def get_observer(self):
        location = EarthLocation(lat=self.latitude * u.deg, lon=self.longitude * u.deg, height=520 * u.m)
        return Observer(location=location, name="AstroTerip")

    def get_zoned_time(self, utc_date_time):
        utc_date_time_str = utc_date_time.strftime("%Y-%m-%d %H:%M:%S")
        time = Time(utc_date_time_str, format='iso', scale='utc', out_subfmt='date*')
        time_zone = pytz.timezone(self.timeZone)
        zoned_time = time.to_datetime(time_zone)
        return zoned_time

def main(args):
    moon = Moon('Australia/Melbourne', -37, 145)

    if args.action[0] == "MOONILLUM":
        illuminated_fraction = moon.get_moon_illumination(datetime.datetime.utcnow())
    if args.action[0] == "MOONALTAZ":
        illuminated_fraction = moon.get_moon_altaz(datetime.datetime.utcnow())
    if args.action[0] == "MOON_NEXT_RISE_DATETIME":
        illuminated_fraction = moon.get_next_rise(datetime.datetime.utcnow())
    if args.action[0] == "MOON_NEXT_SET_DATETIME":
        illuminated_fraction = moon.get_next_set(datetime.datetime.utcnow())
    if args.action[0] == "MOONRADEC":
        illuminated_fraction = moon.get_ra_dec(datetime.datetime.utcnow())

    exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform moon related functions')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('action', nargs='+', help='MOONILLUM')

    args = parser.parse_args()

    main(args)
