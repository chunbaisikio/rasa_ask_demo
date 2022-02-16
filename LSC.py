#!/usr/bin/env python
# coding=utf-8
'''
Date: 2022-02-15 15:18:04
LastEditors: Chunbai_zz
LastEditTime: 2022-02-15 17:40:04
Description: message
'''
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-03-20
# Project: LSC
# desc: LCS

def LCS_list(s1,list):
    result = []
    for item in list:
        result_lcs = LCS(s1,item.name)
        if len(result_lcs) > 0:
            score = len(result_lcs)/len(s1)
            result.append([item,result_lcs,score,item])
        else:
            pass
    return sorted(result,key=lambda x: x[2], reverse=True)



def LCS(s1, s2):
    size1 = len(s1) + 1
    size2 = len(s2) + 1
    # 程序多加一行，一列，方便后面代码编写
    chess = [[["", 0] for j in list(range(size2))] for i in list(range(size1))]
    for i in list(range(1, size1)):
        chess[i][0][0] = s1[i - 1]
    for j in list(range(1, size2)):
        chess[0][j][0] = s2[j - 1]
    for i in list(range(1, size1)):
        for j in list(range(1, size2)):
            if s1[i - 1] == s2[j - 1]:
                chess[i][j] = ['↖', chess[i - 1][j - 1][1] + 1]
            elif chess[i][j - 1][1] > chess[i - 1][j][1]:
                chess[i][j] = ['←', chess[i][j - 1][1]]
            else:
                chess[i][j] = ['↑', chess[i - 1][j][1]]
    i = size1 - 1
    j = size2 - 1
    s3 = []
    while i > 0 and j > 0:
        if chess[i][j][0] == '↖':
            s3.append(chess[i][0][0])
            i -= 1
            j -= 1
        if chess[i][j][0] == '←':
            j -= 1
        if chess[i][j][0] == '↑':
            i -= 1
    s3.reverse()
    return s3