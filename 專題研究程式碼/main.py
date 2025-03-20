import visial_model
from visial_model import visial
from tello_control import stream_tello_reaction_test,tello_record,tello_main_reaction
import threading
import time
import cv2
import tinkerGUI_easy

face_bbox = None  # 臉框座標，格式為 (左上角座標, 右下角座標)
face_width = 0  # 臉框寬度
face_height = 0  # 臉框高度

def Description():
    print("記得將tello放置於地上並且距離自己一小段距離")
    print("請確認tello面向自己，沒有的話我不敢保證發生甚麼事")
    print("發生錯誤或是失控或是測試結束，請立即按下Q鍵會強行降落和結束程式")
    print("最後請確保程式執行時，浮標沒有輸入中、輸入法為英文，程式照理說將在3秒後啟動")
    time.sleep(3)
    print("程式開始執行")
def eyes():

    visial()

def body():

    while True:
        time.sleep(1)
        global face_bbox, face_height, face_width
        face_bbox = visial_model.face_bbox  # 臉框座標，格式為 (左上角座標, 右下角座標)
        face_width = visial_model.face_width  # 臉框寬度
        face_height = visial_model.face_height  # 臉框高度
        print(face_bbox, face_width, face_height)
        cv2.waitKey(1)  # 等待按鍵輸入
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
def face():
    app=tinkerGUI_easy.App()
    app.mainloop()
def act():
    #stream_tello_reaction_test()
    tello_main_reaction()

def recording():
    tello_record()

thread_1 = threading.Thread(target=eyes)
thread_2 = threading.Thread(target=body)
thread_3 = threading.Thread(target=face)
thread_4 = threading.Thread(target=act)
thread_6 = threading.Thread(target=recording)
if __name__ == '__main__':

    a=int(input("啟動按1"))
    if a==1:
        """
        Description()
        """
        thread_3.start()
        thread_4.start()
        thread_1.start()
        thread_2.start()
        thread_6.start()

        thread_1.join()
        thread_2.join()
        thread_3.join()
        thread_4.join()
        thread_6.join()
    else:
        print("傻逼東西 再見")





