import math

# naive attempt helper functions
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
