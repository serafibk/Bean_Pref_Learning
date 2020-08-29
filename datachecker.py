import json
import os

root = r"/Users/serafinakamp/Desktop/Bean_Pref_Learning/roasting_dnn"
filename = os.path.join(root,"bean_data_actual/BEANSFINAL_ACTUAL0.json")
with open(filename,"r") as f:
    beans = json.load(f)
other_file = os.path.join(root,"bean_data_actual/BEANSNORM_ACTUAL0.json")
with open(other_file,"r") as f:
    ref_bean = json.load(f)
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
new_beans=[]
count=0
for i,bean in enumerate(beans):
    origin = bean["Origin"]
    found=False
    for char in origin:
        if char == ";":
            print(origin)
            print(ref_bean[i]["Origin"])
            count=count+1
            found=True
            break
    if not found:
        if ref_bean[i]["Origin"][0] == 0.47407365999999995 and ref_bean[i]["Origin"][1] == -0.46173752888888886:
            print("EDGE CASEvvvv")
            print(origin)
            count=count+1
        else:
            new_beans.append(ref_bean[i])

otherfile = os.path.join(root,"bean_data_actual/BEANSNORM_ACTUAL0.json")
with open(otherfile,"w",encoding="utf-8") as out:
    json.dump(new_beans,out,ensure_ascii=False)

#print(count," of ", len(beans)," contaminated:(")
