import pandas as pd
import os
import numpy as np
import json
import networkx as nx
import time
# from python.query import Test

# CSV_PATH='D:/SimGNNDATA/CSVFiles' #기존 CSV File Folder 경로
CSV_PATH="../resource/CSVFiles" #기존 CSV파일 Folder경로
# JSON_PATH='D:/SimGNNDATA/Test' #새로이 저장할 Json File Folder 경로
JSON_PATH = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/resource/JSONFiles" #새로이 저장할 Json File Folder 경로

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def csvToJson(csvFiles):
  start = time.time()
  print("🚀 PROCESSING(2): csvFiles To Json")
  rtnJson = []
  pairNames = []
  for i,filei in enumerate(csvFiles):
      data = dict()
      df1= pd.read_csv(os.path.join(CSV_PATH,filei+'.csv'))
      data["graph_1"]=np.c_[df1['ID_encode'].tolist(),df1['Adj_ID_encode'].tolist()]
      data["labels_1"]=df1[['Label', 'ID_encode']].drop_duplicates().sort_values(by=['ID_encode'])['Label'].astype(str).tolist()
      graph_1=nx.from_pandas_edgelist(df1,'ID','Adj_ID',create_using=nx.Graph())
      for j,filej in enumerate(csvFiles[i+1:]):
          df2= pd.read_csv(os.path.join(CSV_PATH,filej+'.csv'))
          data["graph_2"]=np.c_[df2['ID_encode'].tolist(),df2['Adj_ID_encode'].tolist()]
          data["labels_2"]=df2[['Label', 'ID_encode']].drop_duplicates().sort_values(by=['ID_encode'])['Label'].astype(str).tolist()
          graph_2=nx.from_pandas_edgelist(df2,'ID','Adj_ID',create_using=nx.Graph())
          for v in nx.optimize_graph_edit_distance(graph_1, graph_2):
              max2 = v
              break
          data["ged"]=max2 
          
          # 파일포인터 생성하여 JSONfiles 쓰고 닫기
          # with open(JSON_PATH+"/"+filei.split(sep='.')[0]+"&"+filej.split(sep='.')[0]+".json",'w') as f:
          #     json.dump(data, f, cls=NumpyEncoder)
          #     f.close()
          #     print(f,'----------------------------------------')

          pairNames.append(filei.split(sep='.')[0]+"&"+filej.split(sep='.')[0])
          rtnJson.append(json.dumps(data, cls=NumpyEncoder))
  print(f"⏰ pair_csv_to_json.py: {time.time() - start}")
  return [pairNames ,rtnJson]