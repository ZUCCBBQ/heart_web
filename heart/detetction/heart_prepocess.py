import cv2
import os
import numpy as np



def video_to_frame(video_location):
    framepath = video_location.replace("video", "frames")
    croppath = video_location.replace("video", "crop")
    print(croppath)
    if os.path.exists(framepath):
        pass
    else:
        os.makedirs(framepath)
    if os.path.exists(croppath):
        pass
    else:
        os.makedirs(croppath)
    video_dir = video_location + "\\" + os.listdir(video_location)[0]

    cap = cv2.VideoCapture(video_dir)
    # 是否成功打开视频
    flag = 0
    if cap.isOpened():
        flag = 1
    else:
        flag = 0
    # 视频帧总数
    i = 0
    imgPath = ""
    if flag == 1:
        while True:
            ret, frame = cap.read()
            # 读取视频帧
            if ret == False:
                # 判断是否读取成功
                break
            i += 1
            # 使用i为图片命名
            imgPath = framepath + "\\" + "%s.png" % str(i)
            # 将提取的视频帧存储进imgPath
            cv2.imwrite(imgPath, frame)
    else:
        pass

    frame_image_dir = os.listdir(framepath)
    for item in frame_image_dir:
        imagepath_raw = framepath + "\\" + item
        image = cv2.imread(imagepath_raw, 1)
        height, width, mode = image.shape
        a = int(height / 2 - 400)
        b = int(height / 2 + 400)
        c = int(width / 2 - 450)
        d = int(width / 2 + 450)
        cropimage = image[a:b, c:d]
        cv2.imwrite(croppath + "\\" + item, cropimage)
    return croppath