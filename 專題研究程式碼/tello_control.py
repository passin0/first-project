from djitellopy import Tello
import time
import cv2
import data


face_bbox = None  # 臉框座標，格式為 (左上角座標, 右下角座標)
face_width = 0  # 臉框寬度
face_height = 0  # 臉框高度


def takeoff_test():
    tello=Tello()
    tello.connect()
    print("tello connect")
    time.sleep(2)
    tello.takeoff()
    time.sleep(1)
    tello.land()
    time.sleep(2)
    print("tello turnoff")
    tello.disconnect()

def stream_test():
    tello=Tello()
    tello.connect()
    print("tello is connected")
    tello.streamon()
    time.sleep(2)
    print("start")
    cv2.namedWindow("telloo")
    while True:
        if tello.get_frame_read() is not None:
            data.running=True
            # 獲取視訊幀
            frame = tello.get_frame_read().frame
            data.cap=frame

            inverted_frame= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            # 顯示視訊幀
            cv2.imshow("telloo", inverted_frame)
            cv2.waitKey(1)  # 等待按鍵輸入
        else:
            print("Camera not started!")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
def tello_record():
    print("空白鍵可以開關錄影")
    width, height = 960, 720
    fps = 30

    # 建立影片寫入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None
    recording = False
    a=0
    # 按下空白鍵開始/結束錄影
    while True:
        if data.model_on is True:
            frame = data.cap
            inverted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(inverted_frame, (width, height))

            # 录制开始
            if data.recording==True:
                if not recording:
                    out = cv2.VideoWriter(f'output{a}.mp4', fourcc, fps, (width, height))
                    recording = True
                    data.recording=False
                    print("開始錄影...")
                else:
                    out.release()
                    recording = False
                    data.recording=False
                    print("錄影結束！")
                    a+=1

            # 录制中，在右上角繪製紅色圓形
            if recording:
                cv2.circle(frame, (width - 50, 50), 20, (0, 0, 255), -1)
                out.write(frame)

            data.recording_cap=frame

            # 按下"q"鍵退出程式
            if cv2.waitKey(1) == ord('q'):
                break
    # 關閉視窗和影片寫入器
    cv2.destroyAllWindows()
    if out is not None:
        out.release()
def stream_tello_reaction_test():
    tello = Tello()
    tello.connect()
    print("tello is connected")
    tello.streamon()
    print("Tello目前電量:",tello.get_battery(),"%")
    preserved_face_width = None
    preserved_face_height = None
    while True:

        if tello.get_frame_read() is not None:
            data.tello_on=True
            frame = tello.get_frame_read().frame
            data.cap = frame
            if data.model_on is True:
                global face_bbox, face_width, face_height
                face_bbox = data.face_bbox
                face_width = data.face_width
                face_height = data.face_height
                # 計算偏移量
                # 計算目標人臉中心與畫面中心的偏移量
                target_x = (face_bbox[0][0] + face_bbox[1][0]) // 2
                target_y = (face_bbox[0][1] + face_bbox[1][1]) // 2

                x_offset = target_x - frame.shape[1] // 2
                y_offset = target_y - frame.shape[0] // 2
                if preserved_face_height is None:
                    preserved_face_width, preserved_face_height = face_width, face_height

                width_change = face_width - preserved_face_width
                height_change = face_height - preserved_face_height

                preserved_face_width, preserved_face_height = face_width, face_height

                # 根據長寬變化進行控制
                threshold_width_change = 10  # 長度變化閥值
                threshold_height_change = 10  # 寬度變化閥值

                if width_change > threshold_width_change and height_change > threshold_height_change:
                    print("tello: move back")
                elif width_change < -threshold_width_change and height_change < -threshold_height_change:
                    print("tello: move forward")
                else:
                    print("tello: no move")
                # 根據偏移量控制Tello移動
                if abs(x_offset) > face_width // 2:
                    # 需要左右移動
                    if x_offset < 0:

                        print("tello: move left")
                    else:

                        print("tello: move right")
                else:

                    print("tello: no move")
                if abs(y_offset) > face_height // 2:
                    # 需要上下移動
                    if y_offset < 0:

                        print("tello: move up")
                    else:

                        print("tello: move down")
                else:
                    print("tello:no move")

            else:
                print("tello no frame!")
            cv2.waitKey(1)  # 等待按鍵輸入
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    tello.streamoff()
    print("tello turnoff")
    tello.disconnect()
def tello_main_reaction():
    tello = Tello()
    tello.connect()
    print("tello is connected")
    tello.streamon()
    print("Tello目前電量:", tello.get_battery(), "%")
    data.battery=tello.get_battery()
    data.tello_connected=True
    preserved_face_width = None
    preserved_face_height = None
    move_speed = 5
    a=None
    times=0
    stop=0
    b=0#是否起飛
    while True: #起飛了 正在非 停止
        data.battery=tello.get_battery()
        if tello.get_frame_read() is not None:
            if a is None:
                a = input("tello frame is on press 1 to start")
                data.tello_on = True
            time.sleep(0.1)
            frame = tello.get_frame_read().frame
            data.cap = frame

        if data.tello_state == "tookoff" and data.tello_model=="track":
            if b==0:
                print("tello is ready to takeoff")
                time.sleep(1)
                print("takeoff")
                tello.takeoff()
                time.sleep(2)
                print("takeoff done")
                b=1
                data.tello_state = 'stoped'
            tello.send_rc_control(0, -1, 0, 0)
            if data.model_on is True:
                global face_bbox, face_width, face_height
                face_bbox = data.face_bbox
                face_width = data.face_width
                face_height = data.face_height
                # 計算偏移量
                # 計算目標人臉中心與畫面中心的偏移量
                target_x = (face_bbox[0][0] + face_bbox[1][0]) // 2
                target_y = (face_bbox[0][1] + face_bbox[1][1]) // 2

                x_offset = target_x - frame.shape[1] // 2
                y_offset = target_y - frame.shape[0] // 2
                if preserved_face_height is None:
                    preserved_face_width, preserved_face_height = face_width, face_height

                width_change = face_width - preserved_face_width
                height_change = face_height - preserved_face_height

                preserved_face_width, preserved_face_height = face_width, face_height

                # 根據長寬變化進行控制
                threshold_width_change = 10  # 長度變化閥值
                threshold_height_change = 10  # 寬度變化閥值

                if width_change > threshold_width_change and height_change > threshold_height_change:
                    tello.move_back(move_speed)
                    print("tello: move back")
                elif width_change < -threshold_width_change and height_change < -threshold_height_change:
                    tello.move_forward(move_speed)
                    print("tello: move forward")
                else:

                    print("tello: no move")
                # 根據偏移量控制Tello移動
                if abs(x_offset) > face_width // 2:
                    # 需要左右移動
                    if x_offset < 0:
                        tello.move_left(move_speed)
                        print("tello: move left")
                    else:
                        tello.move_right(move_speed)
                        print("tello: move right")
                else:

                    print("tello: no move")
                if abs(y_offset) > face_height // 2:
                    # 需要上下移動
                    if y_offset < 0:
                        tello.move_up(move_speed)
                        print("tello: move up")
                    else:
                        tello.move_down(move_speed)
                        print("tello: move down")
                else:

                    print("tello:no move")
            else:
                print("model no face or no ans!")
                time.sleep(0.3)
        if data.tello_state=="stoped":
            tello.send_rc_control(0, -1, 0, 0)
            preserved_face_width = None
            preserved_face_height = None
        if data.tello_state=="landed":
            if b == 1:
                print("tello landing")
                tello.land()
                time.sleep(2)
                b=0
        if data.tello_state=="tookoff" and data.tello_model=="WASD":
            key = cv2.waitKey(1) & 0xFF
            if key == ord('w'):
                tello.move_forward(10)
            elif key == ord('s'):
                tello.move_back(10)
            elif key == ord('a'):
                tello.move_left(10)
            elif key == ord('d'):
                tello.move_right(10)
        cv2.waitKey(1)  # 等待按鍵輸入
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord(' '):
            tello.land()
            global stop
            stop=1
            break
        if stop==1:
            tello.land()
            times+=1
            print(f"tello try to land {times}.")
            break
    tello.land()
    time.sleep(2)
    tello.streamoff()
    print("tello turnoff")
    tello.disconnect()







