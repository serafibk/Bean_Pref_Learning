import numpy as np
import os
import json
import random
import math
import matplotlib.pyplot as plt

root = r"/Users/serafinakamp/Desktop/Bean_Pref_Learning/roasting_dnn"
beanfile = os.path.join(root,"bean_data_actual","BEANSNORM_ACTUAL0.json")

#basically precluster the beans naively (each parameter has equal weight)
#bean profile = ([lat,long],agtron,aroma,acidty,body,flavor,aftertaste,withmilk,price)

##AVL TREE IMPLEMENTATION - using decision trees instead
class coffee_tree_bean:
    def __init__(self, value):
        self.value = value #bean profile
        self.left_bean = None
        self.right_bean = None
        self.height = 1

class coffee_tree:
    def __init__(self):
        self.root = None
        self.count = 0

    def get_height(self,bean):
        if bean == None:
            return 0
        if bean.left_bean == None and bean.right_bean == None:
            return  1
        if bean.left_bean == None:
            return 1 + self.get_height(bean.right_bean)
        if bean.right_bean == None:
            return 1 + self.get_height(bean.left_bean)
        return 1 + max(self.get_height(bean.left_bean),self.get_height(bean.right_bean))

    def add_bean_helper(self,root,val):
        if root == None:
            return coffee_tree_bean(val)
        if val >= root.value:
            root.right_bean = self.add_bean_helper(root.right_bean,val)
            root.height = self.get_height(root)
            if abs(self.calc_balance(root)) > 1:
                root = self.rebalance(root)
        if val < root.value:
            root.left_bean = self.add_bean_helper(root.left_bean,val)
            root.height = self.get_height(root)
            if abs(self.calc_balance(root)) > 1:
                root = self.rebalance(root)
        return root


    def add_bean(self,bean,val):
        self.root = self.add_bean_helper(self.root,val)
        self.count = self.count + 1

    def rotate_right(self,root):
        temp_bean = root.left_bean
        root.left_bean = temp_bean.right_bean
        temp_bean.right_bean = root
        return temp_bean

    def rotate_left(self,root):
        temp_bean = root.right_bean
        root.right_bean = temp_bean.left_bean
        temp_bean.left_bean = root
        return temp_bean

    def rebalance(self,root):
        bal = self.calc_balance(root)

        if bal > 1:
            if self.calc_balance(root.right_bean) < 0:
                root.right_bean = self.rotate_right(root.right_bean)
            root = self.rotate_left(root)
        if bal < 1:
            if self.calc_balance(root.left_bean) > 0:
                root.left_bean = self.rotate_left(root.left_bean)
            root = self.rotate_right(root)
        return root

    def calc_balance(self,root):
        return self.get_height(root.right_bean)-self.get_height(root.left_bean)

    def get_root(self):
        return self.root

    #store tree in a list lol
    def harvest_tree(self):
        tree_list = []
        bean_queue=[]
        bean_queue.append(self.root)
        while len(bean_queue) > 0:
            next_bean = bean_queue[0]
            bean_queue.pop(0)
            if next_bean.left_bean != None:
                bean_queue.append(next_bean.left_bean)
            if next_bean.right_bean != None:
                bean_queue.append(next_bean.right_bean)
            tree_list.append(next_bean.value)
        return tree_list

##DECISION TREE IMPLEMENTATION
class decisive_coffee_bean:
    def __init__(self, value=0,attrib=0):
        self.split_value = value
        self.split_attrib = attrib
        self.left_beans = None
        self.right_beans = None

def create_decision_paths(current_bean):
    le_value_decision = decisive_coffee_bean()
    g_value_decision = decisive_coffee_bean()
    current_bean.left_beans = le_value_decision
    current_bean.right_beans = g_value_decision
    return le_value_decision,g_value_decision

#each tree randomly selects 4 attributes
class decisive_coffee_tree:
    def __init__(self, attributes):
        self.attributes = attributes

        ##construct tree
        self.root = decisive_coffee_bean() #first attribute decision
        next_nodes = []
        next_nodes.append(self.root)
        for n in range(2): #change for more attributes
            future_nodes=[]
            while(len(next_nodes)>0):
                next_deccisive_bean = next_nodes[0]
                del next_nodes[0]
                future_bean_le,future_bean_g = create_decision_paths(next_deccisive_bean)
                future_nodes.append(future_bean_le)
                future_nodes.append(future_bean_g)
            for node in future_nodes:
                next_nodes.append(node)


    def split_group(self,attribute_ind, split_val,bean_group):
        left,right=[],[]
        for bean in bean_group:
            if bean[attribute_ind] <= split_val:
                left.append(bean)
            else:
                right.append(bean)
        return left,right

    def gini_ind(self,bean_groups): #bean_groups is a list of subsets of all beans
        #get total amount of beans
        total_beans = 0
        for group in bean_groups:
            total_beans+=len(group)

        gini = 0.0
        #add proportion of each group
        for bean_group in bean_groups:
            group_size = len(bean_group)
            if group_size==0:
                continue
            dislikes_prop = float(sum([not bean[-1] for bean in bean_group]))/group_size
            likes_prop = float(sum([bean[-1] for bean in bean_group]))/group_size

            score=dislikes_prop*dislikes_prop + likes_prop*likes_prop

            #update gini and weight by relative size of group
            gini+=(1-score)*(group_size/total_beans)
        return gini

    def split_beans(self,all_beans):
        split_attrib, split_val, best_gini, best_groups = 0,1,100,None

        #test all attributes (not class)
        for a in self.attributes:
            for bean in all_beans:
                bean_groups = self.split_group(a,bean[a],all_beans)
                gini = self.gini_ind(bean_groups)
                #print('A%d <= %.3f Gini=%.3f' % ((a), bean[a], gini))
                if gini < best_gini:
                    best_gini = gini
                    best_groups = bean_groups
                    split_attrib = a
                    split_val = bean[a]
        return {'index':split_attrib,'value':split_val,'gini':best_gini,'groups':best_groups}

    def get_majority_class(self,beans):
        total = len(beans)
        if total == 0:
            return 0
        if sum([bean[-1] for bean in beans])/total >=0.5:
            return 1
        else:
            return 0

    def update_node_values(self,root,all_beans):
        #if last node - should only have one attribute left
        if not root.left_beans and not root.right_beans:
            split = self.split_beans(all_beans)
            root.split_value = split["value"]#set value to split by
            root.split_attrib = split["index"]

            ##set left and right to be majority class of each split group
            root.left_beans = self.get_majority_class(split["groups"][0])
            root.right_beans = self.get_majority_class(split["groups"][1])

            #print("final split value", root.split_value)
            #print("final feature, ",split["index"])
            print("END SPLIT: ",split["groups"])
            print("class left: ", root.left_beans)
            print("class right: ", root.right_beans)
        else: #otherwise split and update split val of current node
            split = self.split_beans(all_beans)
            root.split_value = split["value"]
            root.split_attrib = split["index"]
            #print("split feature, ", split["index"])
            if not split["groups"]:
                return
            left,right = split["groups"]
            #attributes.remove(split["index"])#can't split along that value any more
            if left: #recurse left
                self.update_node_values(root.left_beans,left)
            if right: #recurse right
                self.update_node_values(root.right_beans,right)

    def print_vals(self):
        print_nodes=[]
        print_nodes.append(self.root)
        while(len(print_nodes)>0):
            next = print_nodes[0]
            if not next == 1 and not next == 0:
                if next.left_beans:
                    print_nodes.append(next.left_beans)
                if next.right_beans:
                    print_nodes.append(next.right_beans)
                print("feature: ",next.split_attrib," val: ",next.split_value)
            else:
                print("class: ", next)
            del print_nodes[0]





def bean_profile(bean,USER_WEIGHT_PROFILE,USER_BIAS_PROFILE):
    attributes = 0
    profile = 0

    #origin
    origin_zero = bean["Origin"][0]
    profile=(profile+origin_zero)*USER_WEIGHT_PROFILE[0]+USER_BIAS_PROFILE[0]
    attributes=attributes+1

    origin_one = bean["Origin"][1]
    profile=(profile+origin_one)*USER_WEIGHT_PROFILE[1]+USER_BIAS_PROFILE[1]
    attributes=attributes+1

    #Agtron
    profile=(profile+bean["Agtron"])*USER_WEIGHT_PROFILE[2]+USER_BIAS_PROFILE[2]
    attributes=attributes+1

    #Aroma
    if bean["Aroma"] != -1:
        profile=(profile+bean["Aroma"])*USER_WEIGHT_PROFILE[3]+USER_BIAS_PROFILE[3]
        attributes=attributes+1

    #aciditiy
    if bean["Acidity"] != -1:
        profile=(profile+bean["Acidity"])*USER_WEIGHT_PROFILE[4]+USER_BIAS_PROFILE[4]
        attributes=attributes+1

    #Body
    if bean["Body"] != -1:
        profile=(profile+bean["Body"])*USER_WEIGHT_PROFILE[5]+USER_BIAS_PROFILE[5]
        attributes=attributes+1

    #Flavor
    if bean["Flavor"] != -1:
        profile=(profile+bean["Flavor"])*USER_WEIGHT_PROFILE[6]+USER_BIAS_PROFILE[6]
        attributes=attributes+1

    #Aftertaste
    if bean["Aftertaste"] != -1:
        profile=(profile+bean["Aftertaste"])*USER_WEIGHT_PROFILE[7]+USER_BIAS_PROFILE[7]
        attributes=attributes+1

    #WithMilk
    if bean["WithMilk"] != -1:
        profile=(profile+bean["WithMilk"])*USER_WEIGHT_PROFILE[8]+USER_BIAS_PROFILE[8]
        attributes=attributes+1

    profile = profile/attributes
    return profile

def get_dist(bean_prof_one,bean_prof_two):
    return abs(bean_prof_one-bean_prof_two)

def classify_bean(bean,coffee_trees,epsilon,USER_WEIGHT_PROFILE,USER_BIAS_PROFILE):
    beanProf = bean_profile(bean,USER_WEIGHT_PROFILE,USER_BIAS_PROFILE)
    if len(coffee_trees) == 0:
        new_tree = coffee_tree()
        new_tree.add_bean(bean,beanProf)
        coffee_trees.append(new_tree)
        return
    min_dist = float('inf')
    tree_ind = -1
    for ind,tree in enumerate(coffee_trees):
        print("TREE: ", ind, " ROOT: ",tree.get_root().value)
        #assume bean at position 0 is average for tree (maybe try to implement avl tree for this)
        dist_to_root = get_dist(beanProf,tree.get_root().value)
        if dist_to_root < min_dist:
            min_dist = dist_to_root
            tree_ind = ind
    #check that min dist is not larger than some epsilon, then add to tree, otherwise create new tree
    if min_dist < epsilon:
        coffee_trees[tree_ind].add_bean(bean,beanProf)
    else:
        new_tree = coffee_tree()
        new_tree.add_bean(bean,beanProf)
        coffee_trees.append(new_tree)

def shuffle_beans(beandata):
    shuffled_bean_data=[]
    while len(beandata)>0:
        next_ind = math.floor(random.random()*len(beandata))
        shuffled_bean_data.append(beandata[next_ind])
        beandata.pop(next_ind)
    return shuffled_bean_data

#gini index is measure of how likely it is for feature to cause wrong prediction




##START CLASSIFYING (this is k means should I try many iterations?)

USER_WEIGHT_PROFILE = [1,1,1,1,1,1,1,1,1]
USER_BIAS_PROFILE = [0,0,0,0,0,0,0,0,0]

#track the kind of bean the user prefers
average_bean = [0,0,0,0,0,0,0,0,0]

epsilon = 0.01 #maybe change or have it learn somehow, let's learn epsilon

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

for i,bean in enumerate(beandata[:10]):
    print("BEAN ",i)
    print(bean["Name"])
    print(bean["Review"])
    print("Roast (normed) ", bean["Agtron"])
    print()

    label = int(input("Like (1) Dislike (0)"))
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
    bean_vector.append(beandata[i]["Label"])
    BEAN_DATA.append(bean_vector)

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


tree = decisive_coffee_tree([0,1,2,3])
#split = tree.split_beans(BEAN_DATA)
#print("A",split["index"]," <= ", split["value"], "Gini: ", split["gini"])
tree.update_node_values(tree.root,BEAN_DATA) #create the decision tree weights based on training data
tree.print_vals() # see the weights
exit()

'''

beandata=shuffle_beans(beandata)

for bean in beandata:
    classify_bean(bean,coffee_trees,epsilon,USER_WEIGHT_PROFILE,USER_BIAS_PROFILE)


for ind, tree in enumerate(coffee_trees):
    print("MIN:",min(tree.harvest_tree())," ROOT:",tree.harvest_tree()[0]," MAX:",max(tree.harvest_tree()))
    print(len(tree.harvest_tree()))

'''
#idea - use random forest where each tree is trained on a different attribute (learn how much influence each tree has)
#features: origin(lat), origin(long), agtron, aroma, acidity, body, aftertaste, wMilk, Flavor
plt.scatter(origin_lat_beans,origin_long_beans,c=origin_label)
plt.show()
