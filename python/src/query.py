#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import glob
import numpy as np
import time
from functools import reduce

# CSV_PATH="D:/SimGNNDATA/CSVFiles" #기존 CSV파일 Folder경로
CSV_PATH = "../resource/CSVFiles"  # CSV파일 Folder경로
CSV_LIST = glob.glob(CSV_PATH + "/*.csv")  # CSV 파일 하나씩 경로 리스트화

CONNECTED_SYMBOL = "-"
DISCONNECTED_SYMBOL = "_"
COMMA_SYMBOL = ","
CONNECTED = "conn"
DISCONNECTED = "discon"
TYPE_SIX = "20_3-1"

def processRequest(request):
  start = time.time()
  print("🚀 PROCESSING(1): making csvFiles")
  Testlist = []

  for relation in request:
    # relation: [1-20, 1-2-3, 1-2-3-4, "1-2,1-3", "1-2,1-3,1-4", type6]
    relation = relation.replace("-", " - ")
    relation = relation.replace("_", " _ ")
    relation = relation.replace(",", " , ")
    relation = relation.split(" ")
    
    subTest = ""
    
    print(relation)
    # TYPE6
    if relation == TYPE_SIX:
      subTest = processDining_Kitchen_Livingroom()
      
    # TYPE1
    elif len(relation) == 3:
      if relation[1] == CONNECTED_SYMBOL:
        type = CONNECTED
      elif relation[1] == DISCONNECTED_SYMBOL:
        type = DISCONNECTED
      label = int(relation[0])
      adjLabel = int(relation[2])
      subTest = processOneRelation(type, label, adjLabel)
      
    # TYPE2
    elif len(relation) == 5:
      label = int(relation[0])
      adjLabel1 = int(relation[2])
      adjLabel2 = int(relation[4])
      subTest = processTwoRelation(label, adjLabel1, adjLabel2)
      
    # TYPE3,4
    elif len(relation) == 7:
      if relation[3] == CONNECTED_SYMBOL:
        label = int(relation[0])
        adjLabel1 = int(relation[2])
        adjLabel2 = int(relation[4])
        adjLabel3 = int(relation[6])
        subTest = processThreeRelation(label, adjLabel1, adjLabel2, adjLabel3)
      elif relation[3] == COMMA_SYMBOL: 
        label = int(relation[0])
        adjLabel1 = int(relation[2])
        adjLabel2 = int(relation[6])
        subTest = processOneRelationWithTwoPair(label, adjLabel1, adjLabel2)

    # TYPE5
    elif len(relation) == 11:
      label = int(relation[0])
      adjLabel1 = int(relation[2])
      adjLabel2 = int(relation[6])
      adjLabel3 = int(relation[10])
      subTest = processOneRelationWithThreePair(label, adjLabel1, adjLabel2, adjLabel3)
    
    Testlist.append(subTest)
  # for loop done
  print(f"⏰ query.py: {time.time() - start}")
  return reduce(np.intersect1d, Testlist)

# TYPE1: 라벨1 - 인접라벨1
# type === discon 인 경우는 현재 2가지 (거실 <-> 식당, 주방 <-> 식당)
def processOneRelation(type, label, adjLabel):
  Test = []
  for CSV in CSV_LIST:
      df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
      FIND = df.loc[(df["Label"] == label) & (df["Adj_Label"] == adjLabel)]["ID_encode"].values
      if type == "conn" and len(FIND) != 0:
          Test.append(CSV.split("/")[-1].split(".")[0])
      elif type == "discon" and len(FIND) == 0:
          Test.append(CSV.split("/")[-1].split(".")[0])
  return Test

# TYPE2: 라벨1 - 인접라벨1 - 인접라벨2
def processTwoRelation(label, adjLabel1, adjLabel2):
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == label) & (df["Adj_Label"] == adjLabel1)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == adjLabel1) & (df["Adj_Label"] == adjLabel2)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test

# TYPE3: 라벨1 - 인접라벨1 - 인접라벨2 - 인접라벨3
def processThreeRelation(label, adjLabel1, adjLabel2, adjLabel3):
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == label) & (df["Adj_Label"] == adjLabel1)][
            "Adj_ID_encode"
        ].values 
        FIND1 = df.loc[(df["Label"] == adjLabel1) & (df["Adj_Label"] == adjLabel2)][
            "ID_encode"
        ].values 

        FIND2 = df.loc[(df["Label"] == adjLabel1) & (df["Adj_Label"] == adjLabel2)][
            "Adj_ID_encode"
        ].values 
        FIND3 = df.loc[(df["Label"] == adjLabel2) & (df["Adj_Label"] == adjLabel3)][
            "ID_encode"
        ].values 

        BOOL_FIND = np.intersect1d(FIND, FIND1)
        BOOL_FIND1 = np.intersect1d(FIND2, FIND3)
        if (len(BOOL_FIND) != 0) & (len(BOOL_FIND1) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test

# TYPE4: 라벨1 - 인접라벨1, 라벨1 - 인접라벨2
def processOneRelationWithTwoPair(label, adjLabel1, adjLabel2):
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == label) & (df["Adj_Label"] == adjLabel1)]["ID_encode"].values
        FIND1 = df.loc[(df["Label"] == label) & (df["Adj_Label"] == adjLabel2)]["ID_encode"].values
        if (len(FIND1) != 0) & (len(FIND) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test

# TYPE5: 라벨1 - 인접라벨1, 라벨1 - 인접라벨2, 라벨1 - 인접라벨3
def processOneRelationWithThreePair(label, adjLabel1, adjLabel2, adjLabel3):
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == label) & (df["Adj_Label"] == adjLabel1)]["ID_encode"].values
        FIND1 = df.loc[(df["Label"] == label) & (df["Adj_Label"] == adjLabel2)]["ID_encode"].values
        FIND2 = df.loc[(df["Label"] == label) & (df["Adj_Label"] == adjLabel3)]["ID_encode"].values
        if (len(FIND1) != 0) & (len(FIND) != 0) & (len(FIND2) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test

# TYPE6: 식당<->주방-거실 유형
def processDining_Kitchen_Livingroom():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 1)]["ID_encode"].values
        FIND1 = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 3)][
            "Adj_ID_encode"
        ].values
        FIND2 = df.loc[(df["Label"] == 20)]["Adj_ID_encode"].values
        BOOL_FIND = np.setdiff1d(FIND, FIND1)
        if (len(BOOL_FIND) != 0) & (len(FIND1) == 0) & (len(FIND2) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test

#############################################
#############################################
########### Old code ########################
#############################################
#############################################

def 거실a식당():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 20)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2. 거실<->식당

# In[9]:


# 거실<->식당이 연결된 관계
def 거실b식당():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 20)]["ID_encode"].values
        if len(FIND) == 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3. 거실a복도

# In[15]:


# 거실a복도가 연결된 관계
def 거실a복도():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 8)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4. 거실a화장실

# In[18]:


# 거실a화장실 연결된 관계
def 거실a화장실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 4)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 5. 거실a방

# In[ ]:


# 거실a방 연결된 관계
def 거실a방():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 2)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 6. 거실a계단

# In[ ]:


# 거실a계단 연결된 관계
def 거실a계단():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 7)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 7. 거실a주방

# In[ ]:


# 거실a주방 연결된 관계
def 거실a주방():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 3)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 8. 거실a현관

# In[ ]:


# 거실a현관 연결된 관계
def 거실a현관():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 0)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 9. 거실a차고지

# In[ ]:


# 거실a차고지 연결된 관계
def 거실a차고지():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 19)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 10. 거실a다용도실

# In[ ]:


# 거실a다용도실 연결된 관계
def 거실a다용도실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 6)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# # 주방

# ### 1. 식당 <-> 주방 - 거실

# In[6]:


# 식당<->주방a거실이 연결된 관계
#TODO: 잘모르겠는 유형1
def 식당b주방a거실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 1)]["ID_encode"].values
        FIND1 = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 3)][
            "Adj_ID_encode"
        ].values
        FIND2 = df.loc[(df["Label"] == 20)]["Adj_ID_encode"].values
        BOOL_FIND = np.setdiff1d(FIND, FIND1)
        if (len(BOOL_FIND) != 0) & (len(FIND1) == 0) & (len(FIND2) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2.주방<->식당

# In[ ]:


# 주방<->식당이 연결된 관계
def 주방b식당():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 20)]["ID_encode"].values
        if len(FIND) == 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3.주방a펜트리실

# In[ ]:


# 주방a펜트리실 연결된 관계
def 주방a펜트리실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 9)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4.주방a차고지

# In[ ]:


# 주방a차고지 연결된 관계
def 주방a차고지():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 19)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 5.주방a복도

# In[ ]:


# 주방a복도 연결된 관계
def 주방a복도():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 8)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 6. 주방a붙박이실

# In[ ]:


# 주방a붙박이실 연결된 관계
def 주방a붙박이실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 11)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 7.주방a다용도실

# In[ ]:


# 주방a다용도실 연결된 관계
def 주방a다용도실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 6)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 8.주방a포치

# In[ ]:


# 주방a포치 연결된 관계
def 주방a포치():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 18)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 9.주방a세탁실

# In[ ]:


# 주방a세탁실 연결된 관계
def 주방a세탁실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 10)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 10.주방a화장실

# In[ ]:


# 주방a화장실 연결된 관계
def 주방a화장실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 4)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# # 식당

# ### 1.식당a복도

# In[ ]:


# 식당a복도 연결된 관계
def 식당a복도():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 8)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2.식당a포치

# In[ ]:


# 식당a포치 연결된 관계
def 식당a포치():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 18)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3.식당a주방

# In[ ]:


# 식당a주방 연결된 관계
def 식당a주방():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 3)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4.식당a주방a복도

# In[ ]:


# 식당a주방a복도이 연결된 관계
def 식당a주방a복도():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 3)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 8)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 5.식당a주방a거실

# In[ ]:


# 식당a주방a거실이 연결된 관계
def 식당a주방a거실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 3)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 1)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 6.복도a식당a주방a거실

# In[34]:


# 복도a식당a주방a거실이 연결된 관계
def 복도a식당a주방a거실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 20)][
            "Adj_ID_encode"
        ].values  # 복도a식당
        FIND1 = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 3)][
            "ID_encode"
        ].values  # 식당a주방

        FIND2 = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 3)][
            "Adj_ID_encode"
        ].values  # 식당a주방
        FIND3 = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 1)][
            "ID_encode"
        ].values  # 주방a거실

        BOOL_FIND = np.intersect1d(FIND, FIND1)
        BOOL_FIND1 = np.intersect1d(FIND2, FIND3)
        if (len(BOOL_FIND) != 0) & (len(BOOL_FIND1) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 7.차고지a식당a주방a거실

# In[37]:


# 차고지a식당a주방a거실이 연결된 관계
def 차고지a식당a주방a거실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 19) & (df["Adj_Label"] == 20)][
            "Adj_ID_encode"
        ].values  # 차고지a식당
        FIND1 = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 3)][
            "ID_encode"
        ].values  # 식당a주방

        FIND2 = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 3)][
            "Adj_ID_encode"
        ].values  # 식당a주방
        FIND3 = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 1)][
            "ID_encode"
        ].values  # 주방a거실

        BOOL_FIND = np.intersect1d(FIND, FIND1)
        BOOL_FIND1 = np.intersect1d(FIND2, FIND3)
        if (len(BOOL_FIND) != 0) & (len(BOOL_FIND1) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 8.식당a계단실

# In[ ]:


# 식당a계단실 연결된 관계
def 식당a계단실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 7)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 9.식당a펜트리실

# In[ ]:


# 식당a팬트리실 연결된 관계
def 식당a팬트리실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 9)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 10.식당a주방a팬트리실

# In[ ]:


# 식당a주방a팬트리실 연결된 관계
def 식당a주방a팬트리실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 3)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 9)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# # 방

# ### 1. 방a드레스룸

# In[ ]:


# 방a드레스룸 연결된 관계
def 방a드레스룸():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 5)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2. 방a드레스룸, 방a화장실

# In[ ]:


# 방a드레스룸,방a화장실 연결된 관계
def 방a드레스룸c방a화장실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 5)]["ID_encode"].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)]["ID_encode"].values
        if (len(FIND1) != 0) & (len(FIND) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3. 거실a방a드레스룸

# In[20]:


# 거실a방a드레스룸이 연결된 관계
def 거실a방a드레스룸():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 2)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 5)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4. 거실a방a화장실

# In[15]:


# 거실a방a화장실 연결된 관계
def 거실a방a화장실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 2)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 5. 거실a방a붙박이장

# In[25]:


def 거실a방a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 2)]["ID_encode"].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 11)][
            "Adj_ID_encode"
        ].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 6. 방a다용도실

# In[ ]:


# 방a다용도실 연결된 관계
def 방a다용도실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 6)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 7. 방a계단

# In[ ]:


# 방a계단 연결된 관계
def 방a계단():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 7)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 8. 방a화장실c 방a붙박이장

# In[ ]:


# 방a붙박이장,방a화장실 연결된 관계
def 방a붙박이장c방a화장실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 11)]["ID_encode"].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)]["ID_encode"].values
        if (len(FIND1) != 0) & (len(FIND) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 9. 방a드레스룸, 방a화장실c 방a복도

# In[ ]:


# 방a드레스룸,방a화장실c방a복도 연결된 관계
def 방a드레스룸c방a화장실c방a복도():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 5)]["ID_encode"].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)]["ID_encode"].values
        FIND2 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 8)]["ID_encode"].values
        if (len(FIND1) != 0) & (len(FIND) != 0) & (len(FIND2) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 10. 방a붙박이장

# In[ ]:


# 방a붙박이장 연결된 관계
def 방a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 11)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# # 화장실

# ### 1.화장실a복도

# In[ ]:


# 화장실a복도 연결된 관계
def 화장실a복도():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 4) & (df["Adj_Label"] == 8)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2.화장실a방

# In[ ]:


# 화장실a방 연결된 관계
def 화장실a방():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 4) & (df["Adj_Label"] == 2)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3.화장실a다용도실

# In[ ]:


# 화장실a다용도실 연결된 관계
def 화장실a다용도실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 4) & (df["Adj_Label"] == 6)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4.화장실a드레스룸

# In[ ]:


# 화장실a드레스룸 연결된 관계
def 화장실a드레스룸():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 4) & (df["Adj_Label"] == 5)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 7.방a화장실a드레스룸

# In[ ]:


# 방a화장실a드레스룸 연결된 관계
def 방a화장실a드레스룸():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 4) & (df["Adj_Label"] == 5)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 8.복도a방a화장실

# In[ ]:


# 복도a방a화장실 연결된 관계
def 복도a방a화장실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 2)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 9.거실a화장실a복도

# In[ ]:


# 거실a화장실a복도 연결된 관계
def 거실a화장실a복도():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 4)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 4) & (df["Adj_Label"] == 8)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 10.차고지a화장실

# In[ ]:


# 차고지a화장실 연결된 관계
def 차고지a화장실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 19) & (df["Adj_Label"] == 4)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# # 복도

# ### 1.복도a방

# In[43]:


# 복도a방 연결된 관계
def 복도a방():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 2)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2.복도a붙박이장

# In[ ]:


# 복도a붙박이장 연결된 관계
def 복도a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 11)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3.복도a방a붙박이장

# In[ ]:


# 복도a방a붙박이장 연결된 관계
def 복도a방a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 2)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 11)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4.거실a복도a차고지

# In[ ]:


# 거실a복도a차고지 연결된 관계
def 거실a복도a차고지():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 8)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 19)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 5.복도a계단

# In[ ]:


# 복도a계단 연결된 관계
def 복도a계단():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 7)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 6.복도a다용도실

# In[ ]:


# 복도a다용도실 연결된 관계
def 복도a다용도실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 6)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 7.복도a현관

# In[ ]:


# 복도a현관 연결된 관계
def 복도a현관():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 0)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 8.복도a복도

# In[ ]:


# 복도a복도 연결된 관계
def 복도a복도():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 8)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 9.복도a방a드레스룸

# In[ ]:


# 복도a방a드레스룸 연결된 관계
def 복도a방a드레스룸():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 2)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 5)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 10.복도a세탁실

# In[ ]:


# 복도a세탁실 연결된 관계
def 복도a세탁실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 10)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# # 현관

# ### 1.현관a방

# In[ ]:


# 현관a방 연결된 관계
def 현관a방():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 0) & (df["Adj_Label"] == 2)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2.현관a붙박이장

# In[ ]:


# 현관a붙박이장 연결된 관계
def 현관a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 0) & (df["Adj_Label"] == 11)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3.현관a복도a거실

# In[ ]:


# 현관a복도a거실 연결된 관계
def 현관a복도a거실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 0) & (df["Adj_Label"] == 8)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 1)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4.현관a포치

# In[ ]:


# 현관a방 연결된 관계
# TODO
def 현관a방():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 0) & (df["Adj_Label"] == 18)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 5.현관a차고지

# In[ ]:


# 현관a방 연결된 관계
def 현관a방():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 0) & (df["Adj_Label"] == 19)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 6.포치a복도a현관

# In[ ]:


# 포치a복도a현관 연결된 관계
def 포치a복도a현관():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 18) & (df["Adj_Label"] == 8)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 0)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 7.현관a방a붙박이장

# In[ ]:


# 현관a방a붙박이장 연결된 관계
def 현관a방a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 0) & (df["Adj_Label"] == 2)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 11)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 8.현관a방a드레스룸

# In[ ]:


# 현관a방a드레스룸 연결된 관계
def 현관a방a드레스룸():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 0) & (df["Adj_Label"] == 8)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 5)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 9.현관a방a화장실a드레스룸

# In[ ]:


# 현관a방a화장실a드레스룸이 연결된 관계
def 현관a방a화장실a드레스룸():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 0) & (df["Adj_Label"] == 2)][
            "Adj_ID_encode"
        ].values  # 현관a방
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)][
            "ID_encode"
        ].values  # 방a화장실

        FIND2 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)][
            "Adj_ID_encode"
        ].values  # 방a화장실
        FIND3 = df.loc[(df["Label"] == 4) & (df["Adj_Label"] == 5)][
            "ID_encode"
        ].values  # 화장실a드레스룸

        BOOL_FIND = np.intersect1d(FIND, FIND1)
        BOOL_FIND1 = np.intersect1d(FIND2, FIND3)
        if (len(BOOL_FIND) != 0) & (len(BOOL_FIND1) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 10.현관a복도a주방

# In[ ]:


# 현관a복도a주방 연결된 관계
def 현관a복도a주방():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 0) & (df["Adj_Label"] == 8)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 3)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# # 계단

# ### 1.계단a현관

# In[ ]:


# 계단a현관 연결된 관계
def 계단a현관():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 7) & (df["Adj_Label"] == 0)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2.계단a식당

# In[ ]:


# 계단a식당 연결된 관계
def 계단a식당():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 7) & (df["Adj_Label"] == 20)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3.계단a주방

# In[ ]:


# 계단a주방 연결된 관계
def 계단a주방():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 7) & (df["Adj_Label"] == 3)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4.계단a다용도실

# In[ ]:


# 계단a다용도실 연결된 관계
def 계단a다용도실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 7) & (df["Adj_Label"] == 6)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 5.계단a화장실

# In[ ]:


# 계단a화장실 연결된 관계
def 계단a화장실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 7) & (df["Adj_Label"] == 4)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 6.계단a현관a포치

# In[ ]:


# 계단a현관a포치 연결된 관계
def 계단a현관a포치():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 7) & (df["Adj_Label"] == 0)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 0) & (df["Adj_Label"] == 18)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 7.계단a방a붙박이장

# In[ ]:


# 계단a방a붙박이장 연결된 관계
def 계단a방a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 7) & (df["Adj_Label"] == 2)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 11)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 8.계단a방a화장실

# In[ ]:


# 계단a방a화장실 연결된 관계
def 계단a방a화장실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 7) & (df["Adj_Label"] == 2)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 9.계단a방a드레스룸

# In[ ]:


# 계단a방a드레스룸 연결된 관계
def 계단a방a드레스룸():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 7) & (df["Adj_Label"] == 2)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 5)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 10.계단a방a화장실a드레스룸

# In[ ]:


# 계단a방a화장실a드레스룸이 연결된 관계
def 계단a방a화장실a드레스룸():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 7) & (df["Adj_Label"] == 2)][
            "Adj_ID_encode"
        ].values  # 계단a방
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)][
            "ID_encode"
        ].values  # 방a화장실

        FIND2 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)][
            "Adj_ID_encode"
        ].values  # 방a화장실
        FIND3 = df.loc[(df["Label"] == 4) & (df["Adj_Label"] == 5)][
            "ID_encode"
        ].values  # 화장실a드레스룸

        BOOL_FIND = np.intersect1d(FIND, FIND1)
        BOOL_FIND1 = np.intersect1d(FIND2, FIND3)
        if (len(BOOL_FIND) != 0) & (len(BOOL_FIND1) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# # 차고지

# ### 1.차고지a다용도실

# In[ ]:


# 차고지a다용도실 연결된 관계
def 차고지a다용도실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 19) & (df["Adj_Label"] == 6)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2.차고지a다용도실a거실

# In[ ]:


# 차고지a다용도실a거실 연결된 관계
def 차고지a다용도실a거실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 19) & (df["Adj_Label"] == 6)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 6) & (df["Adj_Label"] == 1)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3.차고지a다용도실a주방a거실

# In[ ]:


# 차고지a다용도실a주방a거실이 연결된 관계
def 차고지a다용도실a주방a거실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 19) & (df["Adj_Label"] == 6)][
            "Adj_ID_encode"
        ].values  # 차고지a다용도
        FIND1 = df.loc[(df["Label"] == 6) & (df["Adj_Label"] == 3)][
            "ID_encode"
        ].values  # 다용도-주방

        FIND2 = df.loc[(df["Label"] == 6) & (df["Adj_Label"] == 3)][
            "Adj_ID_encode"
        ].values  # 다용도-주방
        FIND3 = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 1)][
            "ID_encode"
        ].values  # 주방a거실

        BOOL_FIND = np.intersect1d(FIND, FIND1)
        BOOL_FIND1 = np.intersect1d(FIND2, FIND3)
        if (len(BOOL_FIND) != 0) & (len(BOOL_FIND1) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4.차고지a복도a방

# In[ ]:


# 차고지a복도a방 연결된 관계
def 차고지a복도a방():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 19) & (df["Adj_Label"] == 8)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 2)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 5.차고지a세탁실

# In[ ]:


# 차고지a다용도실 연결된 관계
def 차고지a다용도실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 19) & (df["Adj_Label"] == 6)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 6.차고지a식당a거실

# In[ ]:


# 차고지a식당a거실 연결된 관계
def 차고지a식당a거실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 19) & (df["Adj_Label"] == 20)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 20) & (df["Adj_Label"] == 1)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 7.차고지a다용도실a주방a식당

# In[ ]:


# 차고지a다용도실a주방a식당이 연결된 관계
def 차고지a다용도실a주방a식당():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 19) & (df["Adj_Label"] == 6)][
            "Adj_ID_encode"
        ].values  # 차고지a다용도
        FIND1 = df.loc[(df["Label"] == 6) & (df["Adj_Label"] == 3)][
            "ID_encode"
        ].values  # 다용도-주방

        FIND2 = df.loc[(df["Label"] == 6) & (df["Adj_Label"] == 3)][
            "Adj_ID_encode"
        ].values  # 다용도-주방
        FIND3 = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 20)][
            "ID_encode"
        ].values  # 주방a식당

        BOOL_FIND = np.intersect1d(FIND, FIND1)
        BOOL_FIND1 = np.intersect1d(FIND2, FIND3)
        if (len(BOOL_FIND) != 0) & (len(BOOL_FIND1) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 8.차고지a계단

# In[ ]:


# 차고지a계단 연결된 관계
def 차고지a계단():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 19) & (df["Adj_Label"] == 7)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 9.차고지a포치

# In[ ]:


# 차고지a포치 연결된 관계
def 차고지a포치():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 19) & (df["Adj_Label"] == 18)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 10.차고지a복도

# In[ ]:


# 차고지a복도 연결된 관계
def 차고지a복도():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 19) & (df["Adj_Label"] == 8)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# # 세탁실

# ### 1.복도a세탁실a욕실

# In[ ]:


# 복도a세탁실a욕실 연결된 관계
def 복도a세탁실a욕실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 10)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 10) & (df["Adj_Label"] == 4)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2. 세탁실a붙박이장

# In[ ]:


# 세탁실a붙박이장 연결된 관계
def 세탁실a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 10) & (df["Adj_Label"] == 11)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3.세탁실a복도a붙박이장

# In[ ]:


# 세탁실a복도a붙박이장 연결된 관계
def 세탁실a복도a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 10) & (df["Adj_Label"] == 8)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 11)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4.세탁실a복도a다용도실

# In[ ]:


# 세탁실a복도a다용도실 연결된 관계
def 세탁실a복도a다용도실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 10) & (df["Adj_Label"] == 8)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 6)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 5.세탁실a복도a방

# In[ ]:


# 세탁실a복도a방 연결된 관계
def 세탁실a복도a방():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 10) & (df["Adj_Label"] == 8)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 2)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 6.복도a세탁실a차고지

# In[ ]:


# 복도a세탁실a차고지 연결된 관계
def 복도a세탁실a차고지():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 10)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 10) & (df["Adj_Label"] == 19)][
            "ID_encode"
        ].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 7.차고지a세탁실a현관

# In[ ]:


# 차고지a세탁실a현관 연결된 관계
def 차고지a세탁실a현관():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 19) & (df["Adj_Label"] == 10)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 10) & (df["Adj_Label"] == 0)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 8.세탁실a복도a화장실

# In[ ]:


# 세탁실a복도a화장실 연결된 관계
def 세탁실a복도a화장실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 10) & (df["Adj_Label"] == 8)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 4)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 9.세탁실a복도a주방

# In[ ]:


# 세탁실a복도a주방 연결된 관계
def 세탁실a복도a주방():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 10) & (df["Adj_Label"] == 8)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 3)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 10.세탁실a복도a거실

# In[ ]:


# 세탁실a복도a거실 연결된 관계
def 세탁실a복도a거실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 10) & (df["Adj_Label"] == 8)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 1)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# # 드레스룸

# ### 1. 화장실a붙박이장a드레스룸

# In[ ]:


# 화장실a붙박이장a드레스룸 연결된 관계
def 화장실a붙박이장a드레스룸():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 4) & (df["Adj_Label"] == 11)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 11) & (df["Adj_Label"] == 5)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2. 복도a방a화장실a드레스룸

# In[ ]:


# 복도a방a화장실a드레스룸이 연결된 관계
def 복도a방a화장실a드레스룸():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 2)][
            "Adj_ID_encode"
        ].values  # 거실a방
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)][
            "ID_encode"
        ].values  # 방a화장실

        FIND2 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)][
            "Adj_ID_encode"
        ].values  # 방a화장실
        FIND3 = df.loc[(df["Label"] == 4) & (df["Adj_Label"] == 5)][
            "ID_encode"
        ].values  # 화장실a드레스룸

        BOOL_FIND = np.intersect1d(FIND, FIND1)
        BOOL_FIND1 = np.intersect1d(FIND2, FIND3)
        if (len(BOOL_FIND) != 0) & (len(BOOL_FIND1) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3. 방a화장실c 방a붙박이장,방a드레스룸

# In[ ]:


# 방a드레스룸,방a화장실c방a붙박이장 연결된 관계
def 방a드레스룸c방a화장실c방a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 5)]["ID_encode"].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)]["ID_encode"].values
        FIND2 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 11)]["ID_encode"].values
        if (len(FIND1) != 0) & (len(FIND) != 0) & (len(FIND2) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4. 거실a방a화장실a드레스룸

# In[ ]:


# 거실a방a화장실a드레스룸이 연결된 관계
def 거실a방a화장실a드레스룸():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 2)][
            "Adj_ID_encode"
        ].values  # 거실a방
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)][
            "ID_encode"
        ].values  # 방a화장실

        FIND2 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)][
            "Adj_ID_encode"
        ].values  # 방a화장실
        FIND3 = df.loc[(df["Label"] == 4) & (df["Adj_Label"] == 5)][
            "ID_encode"
        ].values  # 화장실a드레스룸

        BOOL_FIND = np.intersect1d(FIND, FIND1)
        BOOL_FIND1 = np.intersect1d(FIND2, FIND3)
        if (len(BOOL_FIND) != 0) & (len(BOOL_FIND1) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 5. 드레스룸a세탁실

# In[ ]:


# 드레스룸a세탁실 연결된 관계
def 드레스룸a세탁실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 5) & (df["Adj_Label"] == 10)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# # 붙박이장

# ### 1.계단실-붙박이장

# In[ ]:


# 계단a붙박이장 연결된 관계
def 계단a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 7) & (df["Adj_Label"] == 11)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2.거실a붙박이장

# In[ ]:


# 거실a붙박이장 연결된 관계
def 거실a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 11)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3.화장실a붙박이장

# In[ ]:


# 화장실a붙박이장 연결된 관계
def 화장실a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 4) & (df["Adj_Label"] == 11)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4.방a붙박이장

# In[ ]:


# 방a붙박이장 연결된 관계
def 방a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 11)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 5. 방a화장실c 방a붙박이장,방a복도

# In[ ]:


# 방a복도c방a화장실c방a붙박이장 연결된 관계
def 방a복도c방a화장실c방a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 8)]["ID_encode"].values
        FIND1 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 4)]["ID_encode"].values
        FIND2 = df.loc[(df["Label"] == 2) & (df["Adj_Label"] == 11)]["ID_encode"].values
        if (len(FIND1) != 0) & (len(FIND) != 0) & (len(FIND2) != 0):
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# # 다용도실

# ### 1.다용도실a붙박이장

# In[ ]:


# 다용도실a붙박이장 연결된 관계
def 다용도실a붙박이장():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 6) & (df["Adj_Label"] == 11)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2. 세탁실a다용도실

# In[ ]:


# 세탁실a다용도실 연결된 관계
def 세탁실a다용도실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 10) & (df["Adj_Label"] == 6)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3. 복도a다용도실a차고지

# In[ ]:


# 복도a다용도실a차고지 연결된 관계
def 복도a다용도실a차고지():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 6)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 6) & (df["Adj_Label"] == 19)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4. 주방a다용도실

# In[ ]:


# 주방a다용도실 연결된 관계
def 주방a다용도실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 6)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 5. 주방a다용도실a차고지

# In[ ]:


# 주방a다용도-차고지 연결된 관계
def 주방a다용도실c차고지():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 6)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 6) & (df["Adj_Label"] == 19)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# # 펜트리실

# ### 1. 거실a펜트리실

# In[ ]:


# 거실a펜트리실 연결된 관계
def 거실a펜트리실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 9)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 2. 복도a펜트리실

# In[ ]:


# 복도a펜트리실 연결된 관계
def 복도a펜트리실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 8) & (df["Adj_Label"] == 9)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 3. 거실a주방a펜트리실

# In[ ]:


# 거실a주방a펜트리실 연결된 관계
def 거실a주방a펜트리실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 1) & (df["Adj_Label"] == 3)][
            "Adj_ID_encode"
        ].values
        FIND1 = df.loc[(df["Label"] == 3) & (df["Adj_Label"] == 9)]["ID_encode"].values
        BOOL_FIND = np.intersect1d(FIND, FIND1)
        if len(BOOL_FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 4. 다용도실a펜트리실

# In[ ]:


# 다용도실a펜트리실 연결된 관계
def 다용도실a펜트리실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 6) & (df["Adj_Label"] == 9)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test


# ### 5. 현관a펜트리실

# In[ ]:


# 현관a펜트리실 연결된 관계
def 현관a펜트리실():
    Test = []
    for CSV in CSV_LIST:
        df = pd.read_csv(CSV, index_col=None, usecols=[1, 3, 4, 5])
        FIND = df.loc[(df["Label"] == 0) & (df["Adj_Label"] == 9)]["ID_encode"].values
        if len(FIND) != 0:
            Test.append(CSV.split("/")[-1].split(".")[0])
    return Test
