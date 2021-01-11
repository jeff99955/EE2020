import cv2
import operator
import json
import pygame
import sys, os
from time import time, sleep
from PIL import Image
import random
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json


#設定視窗大小
CLIP_X1,CLIP_Y1,CLIP_X2,CLIP_Y2 = 160,140,400,360

# 讀model
with open('model_trained.json','r') as f:
    trained_model = json.load(f)
loaded_model = model_from_json(trained_model)
loaded_model.load_weights('model_trained.h5')

cap = cv2.VideoCapture(0) # 啟用鏡頭
i = 0 # 記錄新增的image
set_value = 158 # 定義黑白的閥值變數
image_Q = cv2.THRESH_BINARY # 調整二值化的模式

last_str = 0 #上一個輸出的字串

start_time = time()
count = [0] * 8
result_str = {
  '1': '幹',
  '2': '幹你娘',
  '3': '讚',
  '4': '愛你喔',
  '5': '欲甲慶記某',
}
while True:
    _, CameraImage = cap.read() # 讀取鏡頭畫面
    CameraImage = cv2.flip(CameraImage, 1) # 水平翻轉
    cv2.imshow("", CameraImage) # 顯示鏡頭畫面
    cv2.rectangle(CameraImage, (CLIP_X1, CLIP_Y1), (CLIP_X2, CLIP_Y2), (0,255,0) ,1) # 框出ROI位置

    ROI = CameraImage[CLIP_Y1:CLIP_Y2, CLIP_X1:CLIP_X2] # ROI的大小
    ROI = cv2.resize(ROI, (128, 128))  # ROI resize
    ROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY) # ROI 轉灰階
    _, output = cv2.threshold(ROI, set_value, 255, image_Q) # Threshold Binary：二值化，將大於閾值的灰度值設為最大灰度值，小於閾值的值設為0。
    
    ShowROI = cv2.resize(ROI, (256, 256)) # ROI resize
    _, output2 = cv2.threshold(ShowROI, set_value, 255, image_Q) # Black Background is better for prediction
    cv2.imshow("ROI", output2)

    # 需要存dataset時，可以使用下面這三行進行取樣
    # cv2.imwrite('./test/handdata'+str(i)+'.jpg',output2)
    # i += 1
    # cv2.waitKey(100)

    
    result = loaded_model.predict(output.reshape(1,128, 128, 1)) # 若是訓練彩色，則須把1改成3個channel (1,128,128,3) 配合model輸入的dimension
    predict =   { '1':    result[0][0],
                  '2':    result[0][1],    
                  '3':    result[0][2],
                  '4':    result[0][3],
                  '5':    result[0][4],
                  }
    # print(predict)
    predict = sorted(predict.items(), key=operator.itemgetter(1), reverse=True) # 分數較高者會sort至第一位

    # 這邊是取對應預測的image，沒有則是顯示nosign
    """
    if(predict[0][1] == 1.0):
        predict_img  = pygame.image.load(os.getcwd() + '/dataset_2/' + predict[0][0] + '.jpg')
    else:
        predict_img  = pygame.image.load(os.getcwd() + '/dataset_2/nosign.png')
    predict_img = pygame.transform.scale(predict_img, (400, 400))
    screen.blit(predict_img, (0,0))
    pygame.display.flip()
    """

    
    if(predict[0][1] == 1.0):
      count[int(predict[0][0])] += 1
    #   if(predict[0][0]!=last_str):
    #     print(result_str[predict[0][0]])
    #     last_str = predict[0][0]
    # else:
    #     print('No sign')

    # 使用鍵盤功能
    interrupt = cv2.waitKey(10)

    
    if interrupt & 0xFF == ord('q'): # quit
      break
    if time() - start_time > 5:
      break
            

cap.release()
cv2.destroyAllWindows()
print("predict array:", count)
result = result_str[str(count.index(max(count)))]
fd = os.open("tmp", os.O_RDWR, 0o755)
os.write(fd, result.encode("utf-8"))