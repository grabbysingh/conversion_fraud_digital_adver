# -*- coding: utf-8 -*-
"""
Created on Wed May 12 01:35:57 2021

@author: DELL
"""
# 1. imports
import pandas as pd

# 2. function to complete dataset
def ip_data(t_imprid_cr):
    ip = []
    for i in range(len(t_imprid_cr)):
    #for i in range(1):
        a = data.loc[data['imprId'] == t_imprid_cr[i]]
        b = a['clickIp']
        try:
            ip.append(max(b.values))
        except:
            ip.append(0)
    return ip

# 3. save train dataset
def save_train(data):
    data.to_csv('C:/Users/DELL/Desktop/TechGig/times_internet/comp_data/train_data_comp.csv')

# 4. save test data
def save_test(data):
    data.to_csv('C:/Users/DELL/Desktop/TechGig/times_internet/comp_data/test_data_comp.csv')

# main function
if __name__ == "__main__":
    
    data = pd.read_csv('C:/Users/DELL/Desktop/TechGig/times_internet/all_data/data.csv')
    train = pd.read_csv('C:/Users/DELL/Desktop/TechGig/times_internet/all_data/train.csv')
    test = pd.read_csv('C:/Users/DELL/Desktop/TechGig/times_internet/all_data/test.csv')

    train['clickip_cr'] = ip_data(list(train['imprid_cr']))
    test['clickip_cr'] = ip_data(list(test['imprid_cr']))
    
    #save_train(train)
    #save_test(test)