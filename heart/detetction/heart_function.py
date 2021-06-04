import argparse

import numpy as np
import mxnet as mx

import os
from mxnet import gluon, nd, image
from mxnet.gluon.data.vision import transforms
import gluoncv as gcv
gcv.utils.check_version('0.6.0')
from gluoncv.model_zoo import get_model
import cv2
import multiprocessing as mp
import os
import time
import tqdm

from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.utils.visualizer import ColorMode
from demo.predictor import VisualizationDemo


def class_function(crop_location):
    # 输入：1.模型名称，2.模型地址，3.crop地址
    # inference结果作为文件名称

    classes = 3
    class_names = ['RCA','LAD','LCX']
    context = [mx.cpu()]
    # Load Model
    model_name = "densenet121"
    saved_params = "F:\\heart_web\\heart\\detetction\\0.9725-heart-densenet121-143-best.params"
    save_dir= crop_location.replace("crop","class")
    if os.path.exists(save_dir):
        pass
    else:
        os.makedirs(save_dir)
    pretrained = True if saved_params == '' else False
    kwargs = {'classes': classes, 'pretrained': pretrained}
    net = get_model(model_name, **kwargs)

    if not pretrained:
        net.load_parameters(saved_params, ctx = context)

    # Load Images
    dir_list  = os.listdir(crop_location)

    for file_name  in dir_list:
        # print(file_name)
        img = image.imread(crop_location+'\\'+file_name)
        image_read = cv2.imread(crop_location+'\\'+file_name)

        # Transform
        transform_fn = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(256),
            transforms.ToTensor(),
            transforms.Normalize([0.4914, 0.4822, 0.4465], [0.2023, 0.1994, 0.2010])
        ])

        img = transform_fn(img)
        pred = net(img.expand_dims(0))


        ind = nd.argmax(pred, axis=1).astype('int')
        # print('The input picture is classified to be [%s], with probability %.3f.'%
        #     (class_names[ind.asscalar()], nd.softmax(pred)[0][ind].asscalar()))
        text = 'The artery classified to be [%s], with probability %.3f'%(class_names[ind.asscalar()], nd.softmax(pred)[0][ind].asscalar())
        fontFace = cv2.FONT_HERSHEY_TRIPLEX
        fontScale = 0.5
        fontcolor = (0, 0, 255) # BGR
        thickness = 1
        lineType = 4
        bottomLeftOrigin = 1
        # cv2.putText(image_read,text,(0, 400), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 1)
        number = file_name.split(".")[0]
        savename = number+'_'+text+'.png'

        cv2.imwrite(save_dir + '\\'+ savename, image_read)
    return save_dir

def detection_function(location):
    mp.set_start_method("spawn", force=True)
    WINDOW_NAME = "vessel"
    input_conf = location+"\\"

    output_location = input_conf.replace("class","result")
    if os.path.exists(output_location):
        pass
    else:
        os.makedirs(output_location)

    cfg = get_cfg()
    config_file = "F:\\珠海服务器权重备份\\detectron2\\output_R_101_M\\config.yaml"
    opts = ['MODEL.DEVICE', 'cpu', 'MODEL.WEIGHTS', 'F:\\珠海服务器权重备份\\detectron2\\output_R_101_M\\model_final.pth']
    cfg.merge_from_file(config_file)
    cfg.merge_from_list(opts)
    cfg.freeze()

    demo = VisualizationDemo(cfg, instance_mode=ColorMode.SEGMENTATION)

    for imgfile in os.listdir(input_conf):
        # use PIL, to be consistent with evaluation
        img_fullName = os.path.join(input_conf, imgfile)
        img = read_image(img_fullName, format="BGR")
        start_time = time.time()
        predictions, visualized_output = demo.run_on_image(img)

        if output_location:
            if os.path.isdir(output_location):
                assert os.path.isdir(output_location), output_location
                out_filename = os.path.join(output_location, 'test_' + os.path.basename(imgfile))
            else:
                assert len(input_conf) == 1, "Please specify a directory with args.output"
                out_filename = output_location
            visualized_output.save(out_filename)
        else:
            cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
            # cv2.imshow(WINDOW_NAME, visualized_output.get_image()[:, :, ::-1])
            if cv2.waitKey(0) == 27:
                break  # esc to quit
    return output_location

