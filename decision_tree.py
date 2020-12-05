import numpy as np
import os
import json
import random
import math
import matplotlib.pyplot as plt

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
