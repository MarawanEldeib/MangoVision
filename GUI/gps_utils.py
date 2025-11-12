import exifread

def extract_gps_and_datetime(image_path):
    with open(image_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)
        gps_info = {}
        gps_latitude = tags.get('GPS GPSLatitude')
        gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
        gps_longitude = tags.get('GPS GPSLongitude')
        gps_longitude_ref = tags.get('GPS GPSLongitudeRef')
        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = get_decimal_from_dms(gps_latitude.values, gps_latitude_ref.values)
            lon = get_decimal_from_dms(gps_longitude.values, gps_longitude_ref.values)
            gps_info['Latitude'] = lat
            gps_info['Longitude'] = lon
        date_time = tags.get('EXIF DateTimeOriginal')
        return {"Date and Time": date_time, "GPS Info": gps_info}

def get_decimal_from_dms(dms, ref):
    degrees = dms[0].num / dms[0].den
    minutes = dms[1].num / dms[1].den
    seconds = dms[2].num / dms[2].den
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal
