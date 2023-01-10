from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

class Img:
    #Simple organizer that take an image location as an argument
    #Will extract the exif data and store its geolocation data including
    #Latitude, Longitude and direction as well as the file name
    
    fileLocation = "DEFAULT"
    photoName = "DEFAULT"
    photoLatDec = 1.001
    photoLongDec = 1.001
    photoDirDec = "No Direction Data Available"
    containsValidExif = False
    
    def __init__(self, fileLocation):
        self.fileLocation = fileLocation
        self.photoName = str(fileLocation).split("\\").pop()
    
    def getContainsValidExif(self):
        return self.containsValidExif
    
    def getFileLocation(self):
        return self.fileLocation
    
    def getPhotoLat(self):
        return float(self.photoLatDec)
    
    def getPhotoLong(self):
        return float(self.photoLongDec)
    
    def getPhotoDirection(self):
        return self.photoDirDec
    
    def getPhotoName(self):
        return self.photoName
    
    def extractExif(self):
        #Extracts the exif data and sorts throgh the dictionary - returns a dictionary
        
        exif_data = {}
        image = Image.open(self.fileLocation)
        info = image._getexif()
        
        try:
            if info:
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    if decoded == "GPSInfo":
                        gps_data = {}
                        for gps_tag in value:
                            sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                            gps_data[sub_decoded] = value[gps_tag]
                        exif_data[decoded] = gps_data
                    else:
                        exif_data[decoded] = value
            photoLong = exif_data.get('GPSInfo').get('GPSLongitude')
            photoLongRef = exif_data.get('GPSInfo').get('GPSLongitudeRef')
            photoLat = exif_data.get('GPSInfo').get('GPSLatitude')
            photoLatRef = exif_data.get('GPSInfo').get('GPSLatitudeRef')
            
            try:
                self.photoDirDec = exif_data.get('GPSInfo').get('GPSImgDirection')
            except:
                pass
            
            self.photoLongDec = photoLong[0] + (float(photoLong[1])/60) + (float(photoLong[2])/3600)
            self.photoLatDec = photoLat[0] + (float(photoLat[1])/60) + (float(photoLat[2])/3600)
            
            if photoLongRef == 'W':
                self.photoLatDec *= -1
                
            if photoLatRef == 'S':
                self.photoLongDec *= -1
            self.containsValidExif = True
        except:
            pass