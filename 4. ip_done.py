# -*- coding: utf-8 -*-
"""
Created on Thu May 20 20:33:48 2021

@author: DELL
"""

# 1 imports
import pandas as pd
import ipaddress
import re
#import itertools

# 2 data preprocessing

# for clicktimeinmillis done
def click_time(data):
    mean_clicktime = data['clickTimeInMillis_cr'][1]
    #mean_clicktime = data['clickTimeInMillis_cr'].mean()
    data['clickTimeInMillis_cr'].fillna(value=mean_clicktime, inplace=True)
    return data

# for cityid, stateid, countrydimid, ispdim done
def city_state_country_ispdim(data):
    data.dropna(subset=["cityId_cr"], inplace=True)
    return data

# for browserId, modelDimId, osverDimId done
def browser_modeldim_osverdim(data):
    data.dropna(subset=["browserId_cr"], inplace=True)
    return data

# function dealing with ip address
def to_comp_ip(a):
    zero_dot,single_dot,double_dot,ipv4,ipv6 = ([] for i in range(5))
    ip = []
    z_dot = '^\d{1,3}$'
    s_dot = '^\d{1,3}[.]\d{1,3}$'
    d_dot = '^\d{1,3}[.]\d{1,3}[.]\d{1,3}$'
    t_dot = '^\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}$'
    for i in a:
        if re.search(z_dot, i) != None:
            j = re.search(z_dot, i)
            if int(j.string) > 255:
                j = j.string + ':0:0:0:0:0:0:0'
                ip.append(int(ipaddress.IPv6Address(j)))
            else:
                j = j.string + '.0.0.0'
                ip.append(int(ipaddress.IPv4Address(j)))
        elif re.search(s_dot, i) != None:
            j = re.search(s_dot, i)
            j = j.string + '.0.0'
            ip.append(int(ipaddress.IPv4Address(j)))
        elif re.search(d_dot, i) != None:
            j = re.search(d_dot, i)
            j = j.string + '.0'
            ip.append(int(ipaddress.IPv4Address(j)))
        elif re.search(t_dot, i) != None:
            j = re.search(t_dot, i)
            ip.append(int(ipaddress.IPv4Address(i)))
        else:
            ip.append(int(ipaddress.IPv6Address(i)))
    return ip

# for clickip done
def clickip(data):
    data['clickip_cr'].fillna(value='0.0.0.0', inplace=True)
    data['clickip_cr'].replace(to_replace=['0.0', '0'], value='0.0.0.0', inplace=True)
    a = data['clickip_cr'].tolist()
    ipp = to_comp_ip(a)
    data['ip'] = ipp
    return data

# format train dataframe
def format_train(data):
    cols = data.columns.tolist()
    cols = cols[1:4] + cols[-1:] + cols[4:-1]
    data = data[cols]
    return data

# format test dataframe
def format_test(data):
    cols = data.columns.tolist()
    cols = cols[1:5] + cols[-1:] + cols[5:-1]
    data = data[cols]
    return data
    
# save train csv
def save_train(data):
    data.to_csv('C:/Users/DELL/Desktop/TechGig/times_internet/handle_ip/train_ip_done.csv')
    return data

# save test csv
def save_test(data):
    data.to_csv('C:/Users/DELL/Desktop/TechGig/times_internet/handle_ip/test_ip_done.csv')
    return data

# main function
if __name__ == "__main__":
    train = pd.read_csv('C:/Users/DELL/Desktop/TechGig/times_internet/incomp_data/train_miss.csv')
    test = pd.read_csv('C:/Users/DELL/Desktop/TechGig/times_internet/incomp_data/test_miss.csv')
    
    # for train
    train = click_time(train)
    train = city_state_country_ispdim(train)
    train = browser_modeldim_osverdim(train)
    train = clickip(train)
    train = format_train(train)
    #train = save_train(train)

    # for test
    test = click_time(test)
    test = clickip(test)
    test = format_test(test)
    #test = save_test(test)
