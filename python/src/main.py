from typing import OrderedDict
import torch
from param_parser import parameter_parser
from torch.nn import MSELoss
import glob
from utils import *
from simgnn import *
import time
import os


def main(pairNames, test_graphs):
    start = time.time()
    print("🚀 PROCESSING(3): AIModel (Json to fileNames)")

    JSON_PATH = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/files/JSONFiles/"

    set_seed(42)

    # 사용하는 GPU 사양 및 개수 출력
    USE_CUDA = torch.cuda.is_available()
    device = torch.device('cuda:0' if USE_CUDA else 'cpu')
    # print('-----------------------------------------------------')
    # print(USE_CUDA)
    # print('학습을 진행하는 기기:',device)
    # print('cuda index:', torch.cuda.current_device())
    # print('gpu 개수:', torch.cuda.device_count())
    # print('graphic name:', torch.cuda.get_device_name())
    # print('-----------------------------------------------------')

    args=parameter_parser()
    global_labels={'0': 0, '1': 1, '2': 2,'3': 3, '4': 4, '5': 5,'6': 6, '7': 7, '7': 7,'8': 8, '9': 9, '10': 10, '11': 11, '12': 12,'13': 13, '14': 14, '15': 15,'16': 16, '17': 17,'18': 18, '19': 19, '20': 20 }


    teacher_model=SimGNN(args,device).to(device)
    student_model=Student(args,device).to(device)
    

    # model 불러오기
    teacher_weight=torch.load(f'../saved_teacher_models/batch100_epoch200_GCN2_13_large.pth', map_location = device)
    student_weight=torch.load(f'../saved_student_models/batch100_epoch200_GCN2_13_large.pth', map_location = device)
    teacher_model.load_state_dict(teacher_weight)    
    student_model.load_state_dict(student_weight, strict=False)   
    
    with torch.no_grad():
        student_model.tensor_network.weight_matrix.copy_(teacher_weight['tensor_network.weight_matrix'])
        student_model.tensor_network.weight_matrix_block.copy_(teacher_weight['tensor_network.weight_matrix_block'])
        student_model.tensor_network.bias.copy_(teacher_weight['tensor_network.bias'])
        student_model.fully_connected_first.weight.copy_(teacher_weight['fully_connected_first.weight'])
        student_model.fully_connected_first.bias.copy_(teacher_weight['fully_connected_first.bias'])
        student_model.scoring_layer.weight.copy_(teacher_weight['scoring_layer.weight'])
        student_model.scoring_layer.bias.copy_(teacher_weight['scoring_layer.bias'])

    ged_predict_list=[]
    ged_gt_list=[]
    origin_ged=[]
    ged_file_name=[]

    # local testdataset folder 경로
    # ex) test_graphs = glob.glob("C:/TestDatasetFolder/" + "*.json")
    # test_graphs = glob.glob(JSON_PATH + "*.json")

    # for graph_pair in (test_graphs):
    # test_graphs = json.loads(test_graphs)
    for idx, graph_pair in enumerate(test_graphs):
        # data = process_pair(graph_pair) 
        data = json.loads(graph_pair)
        origin_ged.append(data['ged'])
        data = transfer_to_torch(data,global_labels)
        
        try:
            embedding_vector1,embedding_vector2=student_model(data)
        except:
            print('--------------------------------')
            print(graph_pair)
            print(data)    

        prediction= student_model.embedded_forward(embedding_vector1,embedding_vector2)

                
        ged_file_name.append(pairNames[idx])
        ged_gt_list.append(data['target'].item())
        ged_predict_list.append(prediction.item())
    
    ged_file_name=np.array(ged_file_name)
    ged_predict_list=np.array(ged_predict_list)
    ged_gt_list=np.array(ged_gt_list)
    origin_ged=np.array(origin_ged)
    infos = zip(ged_file_name, ged_predict_list)
    infos = sorted(infos, key= lambda x: x[1])
    test_result = []
    for info in infos[:20]: 
        first, second = info[0].split(sep="&")
        test_result.append(first)
        test_result.append(second)
      

    print(f"⏰ main.py: {time.time() - start}")
    # [1-123-1, 1-123-2, 1-123-1, 1-123-2],,,]
    return test_result


    
if __name__=="__main__":
    main()