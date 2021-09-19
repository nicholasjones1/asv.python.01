import argparse
import datetime
from calendar import timegm
from time import localtime, gmtime, mktime

import astropy
import pytz
from astroplan import Observer
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
import astropy.units as u

class SunWatcher:
    def __init__(self, time_zone, latitude, longitude):
        self.timeZone = time_zone
        self.latitude = latitude
        self.longitude = longitude

    def get_zoned_time(self, utc_date_time):
        utc_date_time_str = utc_date_time.strftime("%Y-%m-%d %H:%M:%S")
        time = Time(utc_date_time_str, format='iso', scale='utc', out_subfmt='date*')
        time_zone = pytz.timezone(self.timeZone)
        zoned_time = time.to_datetime(time_zone)
        return zoned_time

    def get_sun_altitude(self, utc_date_time):
        location = EarthLocation(lat=self.latitude * u.deg, lon=self.longitude * u.deg, height=520 * u.m)
        observer = Observer(location=location, name="AstroTerip")
        zoned_time = self.get_zoned_time(utc_date_time)
        sunAltAz = observer.sun_altaz(zoned_time)
        print(str(round(sunAltAz.alt.deg, 2)))
        return sunAltAz.alt.deg

    def is_night(self, utc_date_time):
        location = EarthLocation(lat=self.latitude * u.deg, lon=self.longitude * u.deg, height=520 * u.m)
        observer = Observer(location=location, name="AstroTerip")
        zoned_time = self.get_zoned_time(utc_date_time)
        is_night = observer.is_night(zoned_time, horizon=-18*u.deg)

        # Voyager can pick up these values
        if is_night:
            print("NIGHT")
        else:
            print("NOTDARK")

        return is_night

def main(args):
#    astropy.test()
    sunwatcher = SunWatcher('Australia/Melbourne', -37, 145)

    if args.action[0] == "ISDARK":
        is_night = sunwatcher.is_night(datetime.datetime.utcnow())
    elif args.action[0] == "ALTSUN":
        sunwatcher.get_sun_altitude(datetime.datetime.utcnow())

    exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send a message to Slack')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('action', nargs='+', help='ISDARK | ALTSUN')

    args = parser.parse_args()

    main(args)
