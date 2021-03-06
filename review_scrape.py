from bs4 import BeautifulSoup
import requests
import json
import numpy as np
import os

beansjson=[]
pageNum = 1
counter = 0

url = "https://www.coffeereview.com/review/"
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}

while url:
    print("PAGE: ",pageNum, " of 281")
    page = requests.get(url,headers=header)

    soup = BeautifulSoup(page.content, 'html.parser')

    reviews = soup.findAll("div",{"class":"review-template"})
    reviewPages = soup.findAll("a",{"title":"Read Complete Review"})
    totalReviews = len(reviewPages)
    #how to get specific review
    for i,review in enumerate(reviewPages):
        print("working on review ", str(i+1), " of ", str(totalReviews))
        beanjson={}
        review_page = requests.get(str(review['href']),headers=header)
        review_soup = BeautifulSoup(review_page.content,'html.parser')

        #store name and short review
        name = review_soup.findAll('h1',{"class":"review-title"})
        print(str(name[0])[25:-5])
        beanjson["Name"] = str(name[0])[25:-5]

        reviews = review_soup.findAll('div',{"class":"review-template"})
        print(str(list(reviews[0].children)[-2])[39:-4])
        beanjson["Review"] = str(list(reviews[0].children)[-2])[39:-4]

        #table contents
        tableEntries = review_soup.findAll('tr')
        for entry in tableEntries:
            holder = list(entry.children)
            if str(holder[0]) == "\n":
                beanjson[str(holder[1])[4:-6]] = str(holder[3])[4:-5]
            else:
                beanjson[str(holder[0])[4:-6]] = str(holder[1])[4:-5]
        beansjson.append(beanjson)
    if pageNum%10==0:
        filename = "BEANS_ACTUAL"+str(counter)+".json"
        with open(filename,"w",encoding='utf-8') as out:
            json.dump(beansjson,out,ensure_ascii=False)
        counter=counter+1
        beansjson=[]
        print("DATA RECORDED")
    if pageNum == 281:
        break
    FindUrl = soup.findAll("li",{"class":"pagination-next"})
    url = str(list(FindUrl[0].children)[0]["href"])
    pageNum=pageNum+1


filename = "BEANS"+str(counter)+".json"
with open(filename,"w",encoding='utf-8') as out:
    json.dump(beansjson,out,ensure_ascii=False)




#bean vector structure
#[origin,agtron(normalized),aroma,acidity,body,flavor,aftertaste,price?,sample of review]
