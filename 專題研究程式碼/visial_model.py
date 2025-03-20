import time

import cv2
import mediapipe as mp
import data

face_bbox = None  # 臉框座標，格式為 (左上角座標, 右下角座標)
face_width = 0  # 臉框寬度
face_height = 0  # 臉框高度
def visial():
    # 初始化Mediapipe的FaceMesh

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()

    # 初始化攝像頭視訊擷取
    cap = data.cap
    print("model is activated")
    data.model_activated=True
    while True:
        if data.tello_on is True:
            # 讀取視訊幀

            cap = data.cap
            cap=cv2.cvtColor(cap, cv2.COLOR_BGR2RGB)

            # 將圖像轉換為RGB格式


            # 在Mediapipe中處理圖像
            results = face_mesh.process(cap)

            # 獲取檢測到的人臉關鍵點
            if results.multi_face_landmarks:
                print("read")
                data.model_on=True
                for face_landmarks in results.multi_face_landmarks:
                    # 獲取人臉範圍
                    bbox = get_bounding_box(face_landmarks, cap)

                    # 在畫面上畫出人臉方框
                    cv2.rectangle(cap, bbox[0], bbox[1], (0, 255, 0), 2)

            # 顯示處理後的畫面
            #cv2.imshow('Face Tracking', cap)
            data.prossessed_cap=cap
        else:
            print("haven't gotten answer")
            time.sleep(0.5)
            # 如果按下q鍵，則結束迴圈
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

            # 釋放資源
    cap.release()
    cv2.destroyAllWindows()


def get_bounding_box(face_landmarks, frame):
    # 初始化最小和最大座標
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = 0, 0

    for landmark in face_landmarks.landmark:
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])

        # 更新最小和最大座標
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

        # 計算臉框的寬度和高度
        width = int(max_x - min_x)
        height = int(max_y - min_y)

        # 更新全域變數與data
        global face_bbox, face_width, face_height
        face_bbox = ((int(min_x), int(min_y)), (int(max_x), int(max_y)))
        face_width = width
        face_height = height
        data.face_bbox=face_bbox
        data.face_height=face_height
        data.face_width=face_width

    return ((min_x, min_y), (max_x, max_y))

