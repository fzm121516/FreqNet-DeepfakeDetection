import sys
import time
import os
import csv
import torch
from util import Logger, printSet
from validate import validate
from networks.freqnet import freqnet
from options.test_options import TestOptions
import numpy as np
import random


DetectionTests = {
        #         'ForenSynths': { 'dataroot'   : '/home/fanzheming/zm/NPR-DeepfakeDetection/dataset/ForenSynths8test/ForenSynths',
        #                          'no_resize'  : False, # Due to the different shapes of images in the dataset, resizing is required during batch detection.
        #                          'no_crop'    : True,
        #                        },

        #    'GANGen-Detection': { 'dataroot'   : '/home/fanzheming/zm/NPR-DeepfakeDetection/dataset/GANGen-Detection',
        #                          'no_resize'  : True,
        #                          'no_crop'    : True,
        #                        },
        #  'Diffusion1kStep': {  # 测试集名称
        #     'dataroot': '/home/fanzheming/zm/NPR-DeepfakeDetection/dataset/Diffusion1kStep',  # 数据根路径
        #     'no_resize': False,  # 是否不调整大小
        #     'no_crop': True,  # 是否不裁剪
        # },  'DiffusionForensics': {  # 测试集名称
        #     'dataroot': '/home/fanzheming/zm/NPR-DeepfakeDetection/dataset/DiffusionForensics8test/DiffusionForensics',  # 数据根路径
        #     'no_resize': False,  # 是否不调整大小
        #     'no_crop': True,  # 是否不裁剪
        # },  

        # 'UniversalFakeDetect': {  # 测试集名称
        #     'dataroot': '/home/fanzheming/zm/NPR-DeepfakeDetection/dataset/UniversalFakeDetect',  # 数据根路径
        #     'no_resize': False,  # 是否不调整大小
        #     'no_crop': True,  # 是否不裁剪
        # },   

        #                 'genimages': {  # 测试集名称
        #     'dataroot': '/home/ubuntu/genimagestest/test',  # 数据根路径
        #     'no_resize': False,  # 是否不调整大小
        #     'no_crop': True , # 是否不裁剪
        # }, 

                                        'foren95': {  # 测试集名称
            'dataroot': '/home/ubuntu/jpeg/jpeg95/foren/test',  # 数据根路径
            'no_resize': False,  # 是否不调整大小
            'no_crop': False,  # 是否不裁剪
        },    

                                'foren85': {  # 测试集名称
            'dataroot': '/home/ubuntu/jpeg/jpeg85/foren/test',  # 数据根路径
            'no_resize': False,  # 是否不调整大小
            'no_crop': False,  # 是否不裁剪
        },    
                                'foren75': {  # 测试集名称
            'dataroot': '/home/ubuntu/jpeg/jpeg75/foren/test',  # 数据根路径
            'no_resize': False,  # 是否不调整大小
            'no_crop': False,  # 是否不裁剪
        },    


                                        'unifd95': {  # 测试集名称
            'dataroot': '/home/ubuntu/jpeg/jpeg95/unifd/test',  # 数据根路径
            'no_resize': False,  # 是否不调整大小
            'no_crop': False,  # 是否不裁剪
        },  

                                'unifd85': {  # 测试集名称
            'dataroot': '/home/ubuntu/jpeg/jpeg85/unifd/test',  # 数据根路径
            'no_resize': False,  # 是否不调整大小
            'no_crop': False,  # 是否不裁剪
        },    

                        'unifd75': {  # 测试集名称
            'dataroot': '/home/ubuntu/jpeg/jpeg75/unifd/test',  # 数据根路径
            'no_resize': False,  # 是否不调整大小
            'no_crop': False,  # 是否不裁剪
        },   

        
                 }


opt = TestOptions().parse(print_options=False)
print(f'Model_path {opt.model_path}')

# get model
model = freqnet(num_classes=1)

# from collections import OrderedDict
# from copy import deepcopy
# state_dict = torch.load(opt.model_path, map_location='cpu')['model']
# pretrained_dict = OrderedDict()
# for ki in state_dict.keys():
    # pretrained_dict[ki[7:]] = deepcopy(state_dict[ki])
# model.load_state_dict(pretrained_dict, strict=True)

model.load_state_dict(torch.load(opt.model_path, map_location='cpu'), strict=True)
model.cuda()
model.eval()

for testSet in DetectionTests.keys():
    dataroot = DetectionTests[testSet]['dataroot']
    printSet(testSet)

    accs = [];aps = []
    print(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
    for v_id, val in enumerate(os.listdir(dataroot)):
        opt.dataroot = '{}/{}'.format(dataroot, val)
        opt.classes  = '' #os.listdir(opt.dataroot) if multiclass[v_id] else ['']
        opt.no_resize = DetectionTests[testSet]['no_resize']
        opt.no_crop   = DetectionTests[testSet]['no_crop']
        acc, ap, _, _, _, _ = validate(model, opt)
        accs.append(acc);aps.append(ap)
        print("({} {:12}) acc: {:.2f}; ap: {:.2f}".format(v_id, val, acc*100, ap*100))
    print("({} {:10}) acc: {:.2f}; ap: {:.2f}".format(v_id+1,'Mean', np.array(accs).mean()*100, np.array(aps).mean()*100));print('*'*25) 

