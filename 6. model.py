# -*- coding: utf-8 -*-
"""
Created on Mon May 24 02:06:12 2021

@author: DELL
"""

import pandas as pd
import numpy as np
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score

# 1. preprocessing training data
def train_preproc(data):
    data.drop(['Unnamed: 0','clickip_cr','clmbuserid_cr','imprid_cr'], axis=1, inplace=True)

# 2. preprocessing testing data
def test_preproc(data):
    data.drop(['Unnamed: 0','clickip_cr','clmbuserid_cr','imprid_cr'], axis=1, inplace=True)

# 3. normalizing data
def min_max(data, column):
    for i in column:
        data[i] = MinMaxScaler().fit_transform(np.array(data[i]).reshape(-1,1))
    #return data

# 4. random forest classifier
def rfc(X_tra, y_tra, X_tes):
    class_rfc = RandomForestClassifier(criterion='entropy')
    class_rfc.fit(X_tra, y_tra)
    y_pred = class_rfc.predict(X_tes)
    return y_pred

# 5. confus matrix
def confus_matrix(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    return cm

# 6. save test csv
def save_test_csv(ids, arr):
    main = pd.DataFrame(data={'conversion_fraud':arr})
    final = pd.concat([ids, main], axis=1, join='inner')
    final.to_csv('C:/Users/DELL/Desktop/TechGig/times_internet/final.csv', index=False)

# main function
if __name__ == "__main__":
    train = pd.read_csv('C:/Users/DELL/Desktop/TechGig/times_internet/ip_as_int/train_comp.csv')
    test = pd.read_csv('C:/Users/DELL/Desktop/TechGig/times_internet/ip_as_int/test_comp.csv')
    
    col = ['clientid_cr', 'pubclientid_cr', 'ip', 'siteId_cr', 'goalid_cr', 
           'cityId_cr', 'stateId_cr', 'countryDimId_cr', 'browserId_cr', 
           'adslotdimid_cr', 'clickTimeInMillis_cr', 'itemcolumbiaid_cr', 
           'ispDimId_cr', 'modelDimId_cr', 'osVerDimId_cr']
    
    # for validation
    train_preproc(train)
    min_max(train, col)
    X_val = train.drop(['conversion_fraud'], axis=1)
    y_val = train.iloc[:, -1:]
    
    # train test split
    X_train_val, X_val, y_train_val, y_val = train_test_split(X_val, y_val, test_size=0.25, random_state = 42)
    
    # training random forest classifier
    y_pred_val = rfc(X_train_val, y_train_val, X_val)
    
    # confusion matrix
    val_con = confus_matrix(y_val, y_pred_val)
    
    # metrics for validation
    val_acc = accuracy_score(y_val, y_pred_val)
    val_pre = precision_score(y_val, y_pred_val)
    val_f1 = f1_score(y_val, y_pred_val)
    val_rec = recall_score(y_val, y_pred_val)
    
    
    # for testing
    test_preproc(test)
    min_max(test, col)
    X_train = train.drop(['conversion_fraud'], axis=1)
    y_train = train.iloc[:, -1:]
    X_test = test.drop(['record_id'], axis=1)
    
    # random forest classifier
    y_pred_test = rfc(X_train, y_train, X_test)
    print(Counter(y_pred_test))
    #save_test_csv(test['record_id'], y_pred_test)
