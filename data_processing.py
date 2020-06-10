import os
import json

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
