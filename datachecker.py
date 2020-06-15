import json
import os

root = r"/Users/serafinakamp/Desktop/Bean_Pref_Learning/roasting_dnn"
filename = os.path.join(root,"BEANSFINAL0.json")
with open(filename,"r") as f:
    beans = json.load(f)

'''
newerbeans=[]
for i,bean in enumerate(beans):
    if bean["Origin"][0] == 0.47407365999999995 and bean["Origin"][1]==-0.46173752888888886:
        print("discarded ", i)
        continue
    newerbeans.append(bean)
with open(filename,"w",encoding="utf-8") as out:
    json.dump(newerbeans,out,ensure_ascii=False)
'''
print(beans[147])
