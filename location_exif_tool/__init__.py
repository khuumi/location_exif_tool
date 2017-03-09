import os
from subprocess import Popen, PIPE
import requests


class AddLocationExif(object):
    @staticmethod
    def _get_coordinates_for_address(location_name):
        base = 'https://maps.googleapis.com/maps/api/geocode/json?address='
        response = requests.get(base + location_name).json()
        results = response.get('results')
        if response.get('status') != 'OK' or len(results) == 0:
            return
        location =  results[0].get('geometry', {}).get('location')
        lat = location.get('lat')
        lon = location.get('lng')
        if lat and lon:
            return lat, lon
    

    @staticmethod
    def _add_location_to_photos(file_folder_name, lat, lon):
        # If expressed in decimal form, northern latitudes are positive,
        # southern latitudes are negative. Eastern longitudes are positive, 
        # western longitudes are negative.

        if lat < 0:
            lat_ref = 'S'
        else:
            lat_ref = 'N'
        
        if lon < 0:
            lon_ref = 'W'
        else:
            lon_ref = 'E'

        latitude = '-exif:gpslatitude=%s' % lat
        latitude_ref = '-exif:gpslatituderef=%s' % lat_ref
        longitude = '-exif:gpslongitude=%s' % lon
        longitude_ref = '-exif:gpslongituderef=%s' % lon_ref

        args = ['exiftool', longitude, latitude, 
                latitude_ref, longitude_ref, file_folder_name]
        exiftool = Popen(args, stdin=PIPE, stdout=PIPE)
        stderr, stdout = exiftool.communicate()
        return (stdout, stderr)


    @classmethod
    def process_folder(cls, path):
        '''Will process the subfolders at path to add coordinates to each of 
           the photos based on subfolders name'''

        for sub_folder_name in os.listdir(path):
            lat, lon = cls._get_coordinates_for_address(sub_folder_name)
            combined_path = os.path.join(path, sub_folder_name)
            if os.path.isdir(combined_path):
                cls._add_location_to_photos(path, lat, lon)

                # Now do the grandchildren folders
                for folder_name in os.listdir(combined_path):
                    new_path = os.path.join(combined_path, folder_name)
                    if os.path.isdir(new_path):
                        cls._add_location_to_photos(new_path, lat, lon)
