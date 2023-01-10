# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 11:31:41 2022

@author: JDYKES
"""

from Image import Img
import simplekml
import os

def getImages(directory):
    #Scans the inputted directory as a string to look for files ending in .jpg
    #Returns an array with the directory to all such files
    imageFiles = []
    for filename in os.scandir(directory):
        f = os.path.join(directory, filename)
        
        if (os.path.isfile(f)):
            if(os.path.splitext(f)[1].upper() == '.JPG'):
                imageFiles.append(f)
                
    return imageFiles

def batchKMZ(imageFiles, KMLName):
    noGeoFiles = []
    kml = simplekml.Kml()
    
    for imageName in imageFiles:
        image = Img(imageName)
        image.extractExif()
        
        if image.getContainsValidExif():
            path = kml.addfile(image.getFileLocation())
            pnt = kml.newpoint(name=image.getPhotoName(), 
                         coords=[(-image.getPhotoLong(), -image.getPhotoLat())])
            
            azimuthDescription = '<p> Image Taken Facing Approx: ' + str(image.photoDirDec) + ' Degrees Azimuth </p>'
            pnt.description = '<img src="' + path +'" alt="picture" width="600" height="400" align="center" />' + azimuthDescription
        else:
            noGeoFiles.append(imageName)
    if len(noGeoFiles) > 0:
        print("Could not find geolocation data for the following files: ")
        for file in noGeoFiles:
            print(file)
        print("Files have been ommitted, but KMZ with files containing geolocation data has been created")
    kml.savekmz(KMLName)
     
#TODO: Make system to save KMZ file to specified directory
targetDirectory = input("Input directory > ")
batchKMZ(getImages(targetDirectory), 'test.kmz')

#Take a csv with a list of photo locations and load them into a buffer and then 
#Loop through all of those directories and harvest the geolocation data and put them
#into another csv with name, 