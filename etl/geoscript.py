# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#declare libraries
import shapefile
import sys
import os
import time
import requests
import urllib2
import zipfile
import datetime
import ogr
import csv
import pandas as pd
#define root path
root="/Volumes/Work/Active Projects/DropBox/GapMinder/Github/ddf--gadm--geo_boundaries/output"
#str(sys.argv[1])
#take folder separator as per os
pathspt=os.path.sep
# path of zip files
zipFileURL = "http://biogeo.ucdavis.edu/data/gadm2.8/gadm28.shp.zip"

#check for extraction directories existence
if not os.path.isdir(root+pathspt+'downloaded'):
    os.makedirs(root+pathspt+'downloaded')
    
if not os.path.isdir(root+pathspt+'files'):
    os.makedirs(root+pathspt+'files')
    
#function to download
def downloadFile(url, directory) :
    localFilename = url.split(pathspt)[-1]
    with open(directory + pathspt + localFilename, 'wb') as f:
        start = time.clock()
        r = requests.get(url, stream=True)
        total_length = r.headers.get('content-length')
        dl = 0
        if total_length is None: # no content length header
            f.write(r.content)
        else:
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                f.write(chunk)
                done = int(50 * int(dl) / int(total_length))
                sys.stdout.write("\033[K")
                sys.stdout.write("\r[%s%s] %s bps\r" % ('=' * done, ' ' * (50-done), dl//(time.clock() - start)))
                print ''
    return (time.clock() - start)
    
#download file file only iof not downloaded earlier or if web file has changed recently
outputFilename = root+ pathspt+"downloaded"+pathspt + "gadm28.shp.zip"
if (not os.path.isfile(outputFilename)):
    time_elapsed = downloadFile(zipFileURL,root+pathspt+"downloaded")
    print "Download complete..."
    print "Time Elapsed: " + str(time_elapsed)
    req = urllib2.Request(zipFileURL)
    url_handle = urllib2.urlopen(req)
    headers = url_handle.info()
    etag = headers.getheader("ETag")
    last_modified = headers.getheader("Last-Modified")
    last_modified=last_modified[:-4]
    last_modified=last_modified.replace(",", "", 1)
    text_file = open(root+pathspt+"downloaded"+pathspt+"Zipmd.txt", "w")
    text_file.write(last_modified)
    text_file.close()
else:
    req = urllib2.Request(zipFileURL)
    url_handle = urllib2.urlopen(req)
    headers = url_handle.info()
    etag = headers.getheader("ETag")
    last_modified = headers.getheader("Last-Modified")
    last_modified=last_modified[:-4]
    last_modified=last_modified.replace(",", "", 1)
    file = open(root+pathspt+"downloaded"+pathspt+"Zipmd.txt", 'r')
    extime=file.read()
    zlmt=time.strptime(last_modified,'%a %d %b %Y %X')
    flmt=time.strptime(extime,'%a %d %b %Y %X')
    if ((time.mktime(zlmt)-time.mktime(flmt))>0):
        time_elapsed = downloadFile(zipFileURL,root+pathspt+"downloaded")
        print "Download complete..."
        print "Time Elapsed: " + str(time_elapsed)
        req = urllib2.Request(zipFileURL)
        url_handle = urllib2.urlopen(req)
        headers = url_handle.info()
        etag = headers.getheader("ETag")
        last_modified = headers.getheader("Last-Modified")
        last_modified=last_modified[:-4]
        last_modified=last_modified.replace(",", "", 1)
        text_file = open(root+pathspt+"downloaded"+pathspt+"Zipmd.txt", "w")
        text_file.write(last_modified)
        text_file.close()
        
# extract the data if last modified date in excel within zip is greater than
# last modified date of excel if it exists
fh = open(outputFilename, 'rb')
z = zipfile.ZipFile(fh)
if (os.path.isfile(root+pathspt+ "downloaded"+pathspt+"gadm28.shp"+pathspt+"gadm28.shp")):
    for info in z.infolist():
        zflmt=datetime.datetime(*info.date_time).strftime('%s')
    xllmt=os.path.getmtime(root+pathspt+ "downloaded"+pathspt+"gadm28.shp"+pathspt+"gadm28.shp")
    if (float(zflmt)>xllmt):
        for name in z.namelist():
            outpath = root+pathspt+ "downloaded"+pathspt+"gadm28.shp"
            z.extract(name, outpath)
else:
    for name in z.namelist():
        outpath = root+pathspt+ "downloaded"+pathspt+"gadm28.shp"
        z.extract(name, outpath)
fh.close()

#read the shapefile data
sf = shapefile.Reader(root+pathspt+ "downloaded"+pathspt+"gadm28.shp"+pathspt+"gadm28.shp")

#read and write layers
shpfile=root+pathspt+ "downloaded"+pathspt+"gadm28.shp"+pathspt+"gadm28.shp"
csvfile=root+pathspt+ "files"+pathspt+"gadm28.csv"

#Open files
csvfile=open(csvfile,'wb')
ds=ogr.Open(shpfile)
lyr=ds.GetLayer()

#Get field names
dfn=lyr.GetLayerDefn()
nfields=dfn.GetFieldCount()
fields=[]
for i in range(nfields):
    fields.append(dfn.GetFieldDefn(i).GetName())
#fields.append('kmlgeometry')
csvwriter = csv.DictWriter(csvfile, fields)
try:csvwriter.writeheader() #python 2.7+
except:csvfile.write(','.join(fields)+'\n')

# Write attributes and kml out to csv
for feat in lyr:
    attributes=feat.items()
    geom=feat.GetGeometryRef()
    #attributes['kmlgeometry']=geom.ExportToKML()
    csvwriter.writerow(attributes)

#clean up
del csvwriter,lyr,ds
csvfile.close()

#read back the csv and format the csv
gadmdata=pd.read_csv(root+pathspt+ "files"+pathspt+"gadm28.csv",header=0)
#get country names
countrydf=gadmdata[['ID_0','ISO','NAME_0']].drop_duplicates()
countrydf["ISO1"]=countrydf["ISO"]
countrydf["Varname"]=countrydf["NAME_0"]
countrydf["Type"]="country"
countrydf["EngType"]="country"
countrydf["ParentType"]="continent"
countrydf["ParentEngType"]="continent"
countrydf["Layer"]=0
countrydf["Parent"]="NA"
#get Layer 1
layer1df=gadmdata[["ID_1","ISO","HASC_1","NAME_0","NAME_1","VARNAME_1","TYPE_1","ENGTYPE_1"]].drop_duplicates()
layer1df["Layer"]=1
layer1df["ParentType"]="country"
layer1df["ParentEngType"]="country"
#get Layer 2
layer2df=gadmdata[["ID_2","ISO","HASC_2","NAME_1","NAME_2","VARNAME_2","TYPE_2","ENGTYPE_2","TYPE_1","ENGTYPE_1"]].drop_duplicates()
layer2df["Layer"]=2
#get Layer 3
layer3df=gadmdata[["ID_3","ISO","HASC_3","NAME_2","NAME_3","VARNAME_3","TYPE_3","ENGTYPE_3","TYPE_2","ENGTYPE_2"]].drop_duplicates()
layer3df["Layer"]=3
#get Layer 4
layer4df=gadmdata[["ID_4","ISO","NAME_3","NAME_4","VARNAME_4","TYPE_4","ENGTYPE_4","TYPE_3","ENGTYPE_3"]].drop_duplicates()
layer4df["Layer"]=4
layer4df["HASC_4"]="NA"
#get Layer 3
layer5df=gadmdata[["ID_5","ISO","NAME_4","NAME_5","TYPE_5","ENGTYPE_5","TYPE_4","ENGTYPE_4"]].drop_duplicates()
layer5df["Layer"]=5
layer5df["HASC_5"]="NA"
layer5df["VARNAME_5"]="NA"
#rename all dfs
countrydf.columns=["ID","ISO","NAME","CountryISO","VARNAME","LOCALTYPE","ENGTYPE","ParentLOCALTYPE","ParentENGTYPE","Layer","Parent"]
layer1df.columns=["ID","CountryISO","ISO","Parent","NAME","VARNAME","LOCALTYPE","ENGTYPE","Layer","ParentLOCALTYPE","ParentENGTYPE"]
layer2df.columns=["ID","CountryISO","ISO","Parent","NAME","VARNAME","LOCALTYPE","ENGTYPE","ParentLOCALTYPE","ParentENGTYPE","Layer"]
layer3df.columns=["ID","CountryISO","ISO","Parent","NAME","VARNAME","LOCALTYPE","ENGTYPE","ParentLOCALTYPE","ParentENGTYPE","Layer"]
layer4df.columns=["ID","CountryISO","Parent","NAME","VARNAME","LOCALTYPE","ENGTYPE","ParentLOCALTYPE","ParentENGTYPE","Layer","ISO"]
layer5df.columns=["ID","CountryISO","Parent","NAME","LOCALTYPE","ENGTYPE","ParentLOCALTYPE","ParentENGTYPE","Layer","ISO","VARNAME"]
#append dataframes
finaldf=countrydf.append(layer1df, ignore_index=True)
finaldf=finaldf.append(layer2df, ignore_index=True)
finaldf=finaldf.append(layer3df, ignore_index=True)
finaldf=finaldf.append(layer4df, ignore_index=True)
finaldf=finaldf.append(layer5df, ignore_index=True)
#Create Aliases
finaldf["Alias1"]=finaldf["CountryISO"]+"_"+finaldf["LOCALTYPE"]
finaldf["Alias2"]=finaldf["CountryISO"]+"_"+finaldf["LOCALTYPE"].str[:3]
finaldf["Alias3"]=finaldf["CountryISO"]+"_"+finaldf["ENGTYPE"]
finaldf["Alias4"]=finaldf["CountryISO"]+"_"+finaldf["ENGTYPE"].str[:3]
finaldf["Alias5"]=finaldf["CountryISO"]+"_"+finaldf["LOCALTYPE"]+"_"+finaldf["NAME"].str[:3]
finaldf["Alias6"]=finaldf["CountryISO"]+"_"+finaldf["LOCALTYPE"].str[:3]+"_"+finaldf["NAME"].str[:3]
finaldf["Alias7"]=finaldf["CountryISO"]+"_"+finaldf["ENGTYPE"]+"_"+finaldf["NAME"].str[:3]
finaldf["Alias8"]=finaldf["CountryISO"]+"_"+finaldf["ENGTYPE"].str[:3]+"_"+finaldf["NAME"].str[:3]
finaldf["Alias9"]=finaldf["CountryISO"]+"_"+finaldf["LOCALTYPE"]+"_"+finaldf["NAME"]
finaldf["Alias10"]=finaldf["CountryISO"]+"_"+finaldf["LOCALTYPE"].str[:3]+"_"+finaldf["NAME"]
finaldf["Alias11"]=finaldf["CountryISO"]+"_"+finaldf["ENGTYPE"]+"_"+finaldf["NAME"]
finaldf["Alias12"]=finaldf["CountryISO"]+"_"+finaldf["ENGTYPE"].str[:3]+"_"+finaldf["NAME"]
finaldf["Alias13"]=finaldf["CountryISO"]+"_"+str(finaldf["Layer"])+"_"+finaldf["LOCALTYPE"]+"_"+finaldf["NAME"]
finaldf["Alias14"]=finaldf["CountryISO"]+"_"+str(finaldf["Layer"])+"_"+finaldf["LOCALTYPE"].str[:3]+"_"+finaldf["NAME"]
finaldf["Alias15"]=finaldf["CountryISO"]+"_"+str(finaldf["Layer"])+"_"+finaldf["ENGTYPE"]+"_"+finaldf["NAME"]
finaldf["Alias16"]=finaldf["CountryISO"]+"_"+str(finaldf["Layer"])+"_"+finaldf["ENGTYPE"].str[:3]+"_"+finaldf["NAME"]

#write putput to csv
finaldf.to_csv(root+pathspt+ "files"+pathspt+"out.csv")