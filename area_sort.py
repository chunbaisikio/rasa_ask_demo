#!/usr/bin/env python
# coding=utf-8
'''
Date: 2020-09-23 13:57:09
LastEditors: Chunbai_zz
LastEditTime: 2022-02-16 10:16:38
Description: message
'''
import os
import pymysql
from DBUtils.PooledDB import PooledDB
from LSC import LCS_list
import pickle
areaword = ['市','省','县','州','镇','区','村','乡']
# 连接database
# 数据库配置
# conn =pymysql.Connect(host='47.96.72.168', port=3306, user='root', password='Law@2018', db='law_recom_sys', charset='utf8')
# cursor = conn.cursor()
POOL = PooledDB(
    creator=pymysql,   # 使用链接数据库的模块
    maxconnections=None,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=5,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=10,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=0,

    # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # ping MySQL服务端，检查是否服务可用，如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host='172.27.16.8',
    port=3306,
    user='db_ht_config',
    password='doc3@n89!',
    database='ht_travel',
    charset='utf8')
conn = POOL.connection()
cursor = conn.cursor()

class Node:
    def __init__(self, parent, name, type):
        self.parent = parent
        self.name = name
        self.type = type

def area_name(name):
    for item in areaword:
        if item in name:
            name = name.replace(item,'')
    return name

def area_pickle():
    Node_0 = Node(None,"root",0)
    nodes_list = []
    ## 全分类规则读取
    names = locals()
    select_class_sql = 'select id,parent_id,name,type from base_geo_info where status = 1 and type in (1,2,3,4) ' 
    cursor.execute(select_class_sql)    
    type_list = cursor.fetchall()
    class_1_item = []
    for item_area in type_list:
        names['Node_' + str(item_area[0])] = Node(names['Node_' + str(item_area[1]) ],item_area[2],item_area[3])
        nodes_list.append(names['Node_' + str(item_area[0])])
    with open('area.pickle','wb') as areaFile:
        pickle.dump(nodes_list,areaFile)

def load_area():
    areafile = 'area.pickle'
    global area_pickle_data
    with open(areafile,'rb') as area_Files:
        area_pickle_data = pickle.load(area_Files)
    

def area_transfor(arealist):
    area_return = []    
    type_2_list = [item for item in area_pickle_data if item.type == 2]
    type_3_list = [item for item in area_pickle_data if item.type == 3]
    type_4_list = [item for item in area_pickle_data if item.type == 4]
    type_all_list = [item for item in area_pickle_data if item.type == 4 or item.type == 3]
    for area in arealist:
        area_3_reault = LCS_list(area, type_3_list)
        if len(area_3_reault) > 0 and area_3_reault[0][2] == 1:
            area_result = area_3_reault[0][0].name
            area_return.append(area_result)
    if len(area_return)==0:
        for area in arealist:
                area_2_reault = LCS_list(area, type_2_list)
                area_2_result_best = area_2_reault[0]
                if len(area_2_reault) > 0 and area_2_result_best[2]==1:
                    area_result = '{}的省会'.format(area_2_result_best[3].name)
                area_return.append(area_result)        
        if len(area_return)==0:
            for area in arealist:
                area_4_reault = LCS_list(area, type_4_list)
                area_4_result_best = area_4_reault[0]
                if len(area_4_reault) > 0 and area_4_result_best[2]==1:
                    area_result = area_4_result_best[3].parent.name
                area_return.append(area_result)           
            if len(area_return)==0:
                for area in arealist:
                    area_all_reault = LCS_list(area, type_all_list)
                    area_all_result_best = area_all_reault[0]
                    if area_all_result_best[2]>0.6:
                        if area_all_result_best[3] == 3:
                            area_result = area_all_result_best[3].name
                        elif area_all_result_best[3] == 4:
                            area_result = area_all_result_best[3].parent.name
                        area_return.append(area_result)

    return list(set(area_return))

load_area()
area_transfor(['河南'])
print(1)
