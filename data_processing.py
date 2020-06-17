import numpy as np
import os
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from decimal import Decimal

root = r"/Users/serafinakamp/Desktop/Bean_Pref_Learning/roasting_dnn"
counter = 0

while(1):
    filename = "BEANS"+str(counter)+".json"
    print("working on file ", counter+1, " of 28")
    newbeans = []
    try:
        with open(os.path.join(root,filename),"r") as f:
            beandata = json.load(f)
        for bean in beandata:
            newbean={
                "Origin":"",
                "Agtron":"",
                "Aroma":"",
                "Acidity":"",
                "Body":"",
                "Flavor":"",
                "Aftertaste":"",
                "WithMilk":"",
                "Price":""
            }
            if "Coffee Origin" in bean:
                newbean["Origin"] = bean["Coffee Origin"]
            if "Agtron" in bean:
                newbean["Agtron"] = bean["Agtron"]
            if "Aroma" in bean:
                newbean["Aroma"] = bean["Aroma"][0]
            if "Acidity\n\t\t\t\t\t\t\t\t/Structure\t\t\t\t\t\t\t" in bean:
                newbean["Acidity"] = bean["Acidity\n\t\t\t\t\t\t\t\t/Structure\t\t\t\t\t\t\t"][0]
            if "Acidity /Structure " in bean:
                newbean["Acidity"] = bean["Acidity /Structure "]
            if "Acidity " in bean:
                newbean["Acidity"] = bean["Acidity "]
            if "Body" in bean:
                newbean["Body"] = bean["Body"][0]
            if "Flavor" in bean:
                newbean["Flavor"] = bean["Flavor"][0]
            if "Aftertaste" in bean:
                newbean["Aftertaste"] = bean["Aftertaste"][0]
            if "With Milk" in bean:
                newbean["WithMilk"] = bean["With Milk"][0]
            if "Est. Price" in bean:
                newbean["Price"] = bean["Est. Price"]
            newbeans.append(newbean)
        filename = "BEANSFINAL"+str(counter)+".json"
        with open(filename,"w",encoding="utf-8") as out:
            json.dump(newbeans,out,ensure_ascii=False)
        counter=counter+1
    except:
        print("done processing beans")
        break


def getCoords(roughcoords):
    lat=''
    long=''
    readingLat=False
    readingLong=False
    for c in roughcoords:
        if c=="," and readingLong:
            readingLong=False
        if c=="," and readingLat:
            readingLat=False
            readingLong=True
        if readingLat:
            lat=lat+c
        if readingLong:
            long=long+c
        if c == '@':
            readingLat=True
    return Decimal(lat),Decimal(long[1:])
root = r"/Users/serafinakamp/Desktop/Bean_Pref_Learning/roasting_dnn"
url = "https://www.google.com/maps/"
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}


#converting json data stored in strings to json data with following format
#[(origin lat,origin long),agtron normalized,aroma N, acidity N, body N, flavor N, aftertaste N, w milk N]
#if any of the latter attributes are not available, set to -1 and we will figure out a way to normalize later

counter = 0
beanfilename = "BEANSFINAL"+str(counter)+".json"


while(1):
    try:
        print("working on file ", counter+1," of 27")

        #open bean file to start processing
        with open(beanfilename,"r") as f:
            beans = json.load(f)
        newbeans=[]

        #do stuff with beans
        for beannum,bean in enumerate(beans):
            #set up search object
            driver = webdriver.Safari()
            driver.get(url)
            search = driver.find_element_by_xpath("//input[@id='searchboxinput']")

            print("origin: ",bean["Origin"]," at position ", beannum)
            #handling origin - normalized
            search.send_keys(bean["Origin"],Keys.RETURN)
            time.sleep(5)
            lat,long = getCoords(str(driver.current_url))
            origin = (float(lat)/90.0,float(long)/180.0)
            bean["Origin"] = origin

            #handling agtron - normalized
            agtron = bean["Agtron"]
            num = ''
            denom=''
            NUM=True
            DEN=False
            for c in agtron:
                if DEN:
                    denom=denom+c
                if c=='/':
                    NUM=False
                    DEN=True
                if NUM:
                    num=num+c
            bean["Agtron"] = float(int(num)/int(denom))

            #handling taste palate - normalized
            if bean["Aroma"] != '':
                bean["Aroma"] = float(int(bean["Aroma"])/10)
            else:
                bean["Aroma"] = -1
            if bean["Acidity"] != '':
                bean["Acidity"] = float(int(bean["Acidity"])/10)
            else:
                bean["Acidity"] = -1
            if bean["Body"] != '':
                bean["Body"] = float(int(bean["Body"])/10)
            else:
                bean["Body"] = -1
            if bean["Flavor"] != '':
                bean["Flavor"] = float(int(bean["Flavor"])/10)
            else:
                bean["Flavor"]=-1
            if bean["Aftertaste"] != '':
                bean["Aftertaste"] = float(int(bean["Aftertaste"])/10)
            else:
                bean["Aftertaste"] = -1
            if bean["WithMilk"] != '':
                bean["WithMilk"] = float(int(bean["WithMilk"])/10)
            else:
                bean["WithMilk"] = -1

            #don't change price - wont be part of bean profile
            newbeans.append(bean)
            driver.quit()

        filename = "BEANSFINAL"+str(counter)+".json"
        with open(filename,"w",encoding="utf-8") as out:
            json.dump(newbeans,out,ensure_ascii=False)
        counter=counter+1
        break
    except:
        print("done w preprocessing")
        break
