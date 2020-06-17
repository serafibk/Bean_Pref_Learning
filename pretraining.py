import numpy as np
import os
import json

root = r"/Users/serafinakamp/Desktop/Bean_Pref_Learning/roasting_dnn"
beanfile = os.path.join(root,"bean_data","BEANSFINAL0.json")

#basically precluster the beans naively (each parameter has equal weight)
#bean profile = ([lat,long],agtron,aroma,acidty,body,flavor,aftertaste,withmilk,price)

class coffee_tree_bean:
    def __init__(self, value):
        self.value = value
        self.left_bean = None
        self.right_bean = None
        self.height = 1

class coffee_tree:
    def __init__(self):
        self.root = None
        self.count = 0

    def get_height(bean):
        if bean == None:
            return 0
        if bean.left_bean == None and bean.right_bean == None:
            return  1
        if bean.left_bean == None:
            return 1 + get_height(bean.right_bean)
        if bean.right_bean == None:
            return 1 + get_height(bean.left_bean)
        return 1 + max(get_height(bean.left_bean),get_height(bean.right_bean))

    def add_bean(root,val):
        if root == None:
            return coffee_tree_bean(value)
        if val >= root.value:
            root.right_bean = add_bean(root.right_bean,val)
            root.height = get_height(root)
            if abs(calc_balance(root)) > 1:
                rebalance(root)

        if val < root.value:
            root.left_bean = add_bean(root.left_bean,val)
            root.height = get_height(root)
            if abs(calc_balance(root)) > 1:
                rebalance(root)

    def rotate_right(root):
        temp_bean = root.left_bean
        root.left_bean = temp_bean.right_bean
        temp_bean.right_bean = root
        return temp_bean

    def rotate_left(root):
        temp_bean = root.right_bean
        root.right_bean = temp_bean.left_bean
        temp_bean.left_bean = root
        return temp_bean

    def rebalance(root):
        bal = calc_balance(root)

        if bal > 1:
            if calc_balance(root.right_bean) < 0:
                root.right_bean = rotate_right(root.right_bean)
            root = rotate_left(root)
        if bal < 1:
            if calc_balance(root.left_bean) > 0:
                root.left_bean = rotate_left(root.left_bean)
            root = rotate_right(root)

    def calc_balance(root):
        return get_height(root.right_bean-root.left_bean)

    def get_root():
        return self.root



def bean_profile(bean):
    attributes = 0
    profile = 0

    #origin
    origin_normed = (bean["Origin"][0]+bean["Origin"][1])/2
    profile=profile+origin_normed
    attributes=attributes+1

    #Agtron
    profile=profile+bean["Agtron"]
    attributes=attributes+1

    #Aroma
    if bean["Aroma"] != -1:
        profile=profile+1
        attributes=attributes+1

    #aciditiy
    if bean["Acidity"] != -1:
        profile=profile+bean["Acidity"]
        attributes=attributes+1

    #Body
    if bean["Body"] != -1:
        profile=profile+bean["Body"]
        attributes=attributes+1

    #Flavor
    if bean["Flavor"] != -1:
        profile=profile+bean["Flavor"]
        attributes=attributes+1

    #Aftertaste
    if bean["Aftertaste"] != -1:
        profile=profile+bean["Aftertaste"]
        attributes=attributes+1

    #WithMilk
    if bean["WithMilk"] != -1:
        profile=profile+bean["WithMilk"]
        attributes=attributes+1

    profile = profile/attributes
    return profile

def classify_bean(bean, coffee_trees):
    if len(coffee_trees) == 0:
        coffee_tree = [bean]
        coffee_trees.append(coffee_tree)
        return
    beanProf = bean_profile(bean)
    for coffee_tree in coffee_trees:
        #assume bean at position 0 is average for tree (maybe try to implement avl tree for this)



USER_WEIGHT_PROFILE = [1,1,1,1,1,1,1,1]
USER_BIAS_PROFILE = [0,0,0,0,0,0,0,0]

epsilon = 0.1 #maybe change or have it learn somehow
