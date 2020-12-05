import numpy as np
import os
import json
import random
import math
import matplotlib.pyplot as plt


##AVL TREE IMPLEMENTATION
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
