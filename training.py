import numpy as np
import os
import json
import random
import math
import matplotlib.pyplot as plt
import avl_tree, decision_tree,adaboost,bean_helpers

root = r"/Users/serafinakamp/Desktop/Bean_Pref_Learning/roasting_dnn"
beanfile = os.path.join(root,"bean_data_actual","BEANSNORM_ACTUAL0.json")

#bean profile = ([lat,long],agtron,aroma,acidty,body,flavor,aftertaste,withmilk,price) -- features of each bean


##START CLASSIFYING
if __name__ == "__main__":

    #assuming equal weight of each feature initially
    USER_WEIGHT_PROFILE = [1,1,1,1,1,1,1,1,1]
    USER_BIAS_PROFILE = [0,0,0,0,0,0,0,0,0]

    #track the kind of bean the user prefers
    average_bean = [0,0,0,0,0,0,0,0,0]

    epsilon = 0.01 #maybe change or have it learn somehow

    coffee_trees=[]

    with open(beanfile,"r") as f:
        beandata = json.load(f)


    origin_lat_beans=[]
    origin_long_beans=[]
    origin_label=[]
    agtron_beans=[]
    agtron_label=[]
    aroma_beans=[]
    aroma_label=[]
    acidity_beans=[]
    acidity_label=[]
    body_beans=[]
    body_label=[]
    aftertaste_beans=[]
    aftertaste_label=[]
    flavor_beans=[]
    flavor_label=[]
    wMilk_beans=[]
    wMilk_label=[]

    BEAN_DATA=[]
    BEAN_LABEL=[]

    for i,bean in enumerate(beandata[:20]):
        print("BEAN ",i)
        print(bean["Name"])
        print(bean["Review"])
        print("Roast (normed) ", bean["Agtron"])
        print()

        label = int(input("Like (1) Dislike (-1)"))
        beandata[i]["Label"] = label

        bean_vector=[]
        bean_vector.append(bean["Origin"][0])
        bean_vector.append(bean["Origin"][1])
        bean_vector.append(bean["Agtron"])
        bean_vector.append(bean["Aroma"])
        bean_vector.append(bean["Acidity"])
        bean_vector.append(bean["Body"])
        bean_vector.append(bean["Aftertaste"])
        bean_vector.append(bean["Flavor"])
        bean_vector.append(bean["WithMilk"])
        #bean_vector.append(beandata[i]["Label"])
        BEAN_DATA.append(bean_vector)
        BEAN_LABEL.append(label)

        if bean["Origin"] != -1:
            origin_lat_beans.append(bean["Origin"][0])
            origin_long_beans.append(bean["Origin"][1])
            origin_label.append(beandata[i]["Label"])
        if bean["Agtron"] != -1:
            agtron_beans.append(bean["Agtron"])
            agtron_label.append(beandata[i]["Label"])
        if bean["Aroma"] != -1:
            aroma_beans.append(bean["Aroma"])
            aroma_label.append(beandata[i]["Label"])
        if bean["Acidity"] != -1:
            acidity_beans.append(bean["Acidity"])
            acidity_label.append(beandata[i]["Label"])
        if bean["Body"] != -1:
            body_beans.append(bean["Body"])
            body_label.append(beandata[i]["Label"])
        if bean["Aftertaste"] != -1:
            aftertaste_beans.append(bean["Aftertaste"])
            aftertaste_label.append(beandata[i]["Label"])
        if bean["Flavor"] != -1:
            flavor_beans.append(bean["Flavor"])
            flavor_label.append(beandata[i]["Label"])
        if bean["WithMilk"] != -1:
            wMilk_beans.append(bean["WithMilk"])
            wMilk_label.append(beandata[i]["Label"])


    '''
    DECISION TREES
    tree = decision_tree.decisive_coffee_tree([0,1,2,3])
    #split = tree.split_beans(BEAN_DATA)
    #print("A",split["index"]," <= ", split["value"], "Gini: ", split["gini"])
    tree.update_node_values(tree.root,BEAN_DATA) #create the decision tree weights based on training data
    tree.print_vals() # see the weights
    exit()
    '''
    '''
    AVL TREES
    beandata=bean_helpers.shuffle_beans(beandata)

    for bean in beandata:
        bean_helpers.classify_bean(bean,coffee_trees,epsilon,USER_WEIGHT_PROFILE,USER_BIAS_PROFILE)


    for ind, tree in enumerate(coffee_trees):
        print("MIN:",min(tree.harvest_tree())," ROOT:",tree.harvest_tree()[0]," MAX:",max(tree.harvest_tree()))
        print(len(tree.harvest_tree()))

    '''
    '''
    RANDOM FOREST FEATURE SELECTION
    #idea - use random forest where each tree is trained on a different attribute (learn how much influence each tree has)
    #features: origin(lat), origin(long), agtron, aroma, acidity, body, aftertaste, wMilk, Flavor
    plt.scatter(origin_lat_beans,origin_long_beans,c=origin_label)
    plt.show()
    '''

    ## ADA BOOST attempt
    num_clf = 9
    boosted_beans = adaboost.ADABeans(num_clf,len(BEAN_DATA))
    thetas,alphs = boosted_beans.train_classifiers(BEAN_DATA,BEAN_LABEL)
    print(thetas)
    print(alphs)

    bean = beandata[21]
    bean_vector=[]
    bean_vector.append(bean["Origin"][0])
    bean_vector.append(bean["Origin"][1])
    bean_vector.append(bean["Agtron"])
    bean_vector.append(bean["Aroma"])
    bean_vector.append(bean["Acidity"])
    bean_vector.append(bean["Body"])
    bean_vector.append(bean["Aftertaste"])
    bean_vector.append(bean["Flavor"])
    bean_vector.append(bean["WithMilk"])
    print(bean["Name"])
    print(bean["Review"])
    print("Roast (normed) ", bean["Agtron"])
    print(boosted_beans.predict(bean_vector))
