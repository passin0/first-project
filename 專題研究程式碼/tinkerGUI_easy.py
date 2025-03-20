import customtkinter
import time
import cv2
from PIL import Image, ImageTk
import data

condition = 1


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # 設置視窗大小和標題
        self.geometry("800x600")
        self.title("gala-gala app")

        # 創建加載遮罩
        self.loading_overlay = customtkinter.CTkFrame(self, width=800, height=600, corner_radius=0)
        self.loading_overlay.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

        self.loading_label = customtkinter.CTkLabel(self.loading_overlay, text="Loading...",
                                                    font=customtkinter.CTkFont(size=40, weight="bold"))
        self.loading_label.place(relx=0.5, rely=0.4, anchor=customtkinter.CENTER)

        # 創建進度條
        self.progress_bar = customtkinter.CTkProgressBar(self.loading_overlay, mode="determinate", width=200)
        self.progress_value = 0
        self.progress_bar.set(self.progress_value)
        self.progress_bar.place(relx=0.5, rely=0.65, anchor=customtkinter.CENTER)
        self.little = customtkinter.CTkLabel(self.loading_overlay, text="set...", font=("Arial", 20))  # 作家仔提示用
        self.little.place(relx=0.8, rely=0.95, anchor=customtkinter.CENTER)
        # 模擬加載過程
        self.after(3000, self.update_progress)

        # 創建左欄
        self.grid_columnconfigure(0, weight=0)  # 左側列可伸縮
        self.grid_columnconfigure(1, weight=2)  # 左側列可伸縮
        # create sidebar frame with widgets
        self.sidebar_frame_left = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame_left.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame_left.grid_rowconfigure(4, weight=2)

        self.sidebar_frame_right = customtkinter.CTkFrame(self, width=140, corner_radius=50)
        self.sidebar_frame_right.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame_left, text="haha haha",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame_left, text="take off",
                                                        command=lambda: self.another_botton_event(3))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame_left, text="land",
                                                        command=lambda: self.another_botton_event(4))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame_left, text="stay/go",
                                                        command=lambda: self.another_botton_event(5))
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.button1 = customtkinter.CTkButton(self.sidebar_frame_left, text="record/restore",
                                               command=lambda: self.another_botton_event(1))
        self.button2 = customtkinter.CTkButton(self.sidebar_frame_left, text="change visiol/WASD",
                                               command=lambda: self.another_botton_event(2))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame_left, text="Appearance Mode:",
                                                            anchor="s")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame_left,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame_left, text="UI Scaling:", anchor="s")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame_left,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.co = customtkinter.CTkLabel(self.sidebar_frame_left, text="state:waiting... , battery:X%",
                                         anchor="s")
        self.co.grid(row=11, column=0, padx=20, pady=(20, 10))

        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))
        self.sidebar_frame_left.grid_forget()
        # 123456789
        self.tabview = customtkinter.CTkTabview(self.sidebar_frame_right, width=250)
        self.tabview.add("clear")
        self.tabview.add("track")
        self.tabview.add("record")
        self.tabview.tab("clear").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("track").grid_columnconfigure(0, weight=1)

        self.image_label1 = customtkinter.CTkLabel(self.tabview.tab("clear"), text=" ")
        self.image_label1.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.image_label2 = customtkinter.CTkLabel(self.tabview.tab("track"), text="")
        self.image_label2.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.image_label3 = customtkinter.CTkLabel(self.tabview.tab("record"), text="")
        self.image_label3.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.capture = cv2.VideoCapture(0)
        self.sidebar_frame_right.grid_forget()
        # setting
        self.change_appearance_mode_event("Dark")
        self.button1.configure(state="normal")  # 1
        self.button2.configure(state="normal")  # 2
        self.sidebar_button_1.configure(state="normal")  # 3
        self.sidebar_button_2.configure(state="disabled")  # 4
        self.sidebar_button_3.configure(state="disabled")  # 5

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def update_progress(self):
        word = self.loading_assess()
        self.little.forget()
        self.little = customtkinter.CTkLabel(self.loading_overlay, text=word, font=("Arial", 20))  # 作家仔提示用
        self.little.place(relx=0.8, rely=0.95, anchor=customtkinter.CENTER)

        if word == "connecting Tello.....":
            if self.progress_value < 40:
                self.progress_value += 10
                self.progress_bar.set(self.progress_value / 100)
        elif word == "activating Mediapipe.....":
            if self.progress_value < 90:
                self.progress_value += 10
                self.progress_bar.set(self.progress_value / 100)
        if word == "all done!!!":
            self.progress_value += 10
            self.progress_bar.set(self.progress_value / 100)

        if self.progress_value < 100:
            self.after(100, self.update_progress)
        else:
            self.hide_loading_overlay()

    def hide_loading_overlay(self):
        self.loading_overlay.destroy()
        self.progress_bar.stop()
        self.sidebar_frame_left.grid_configure(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.image_label3.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.button1.grid(row=4, column=0, padx=20, pady=20)
        self.button2.grid(row=5, column=0, padx=20, pady=20)
        self.sidebar_frame_right.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.tabview.pack(side="top", expand=True, pady=(30, 50))
        self.image_label3.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        if cv2.VideoCapture(0) is not None:
            self.update_image()

    def update_image(self):
        # 從攝像頭捕獲影像

        ret, frame = self.capture.read()
        if frame.any() != None:
            # 轉換影像格式並在 GUI 中顯示
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo_image = ImageTk.PhotoImage(image=Image.fromarray(frame))
        else:
            pic = Image.open("no_frame.png")
            photo_image = ImageTk.PhotoImage(pic)
        self.image_label3.configure(image=photo_image)
        self.image_label3.image = photo_image
        self.image_label1.configure(image=photo_image)
        self.image_label1.image = photo_image
        self.image_label2.configure(image=photo_image)
        self.image_label2.image = photo_image
        # 偷偷放在這
        tt = "state:" + data.tello_state + " , battery:" + str(data.battery) + "%"
        self.co.grid_forget()
        self.co.forget()
        self.co = customtkinter.CTkLabel(self.sidebar_frame_left, text=tt,
                                         anchor="s")
        self.co.grid(row=11, column=0, padx=20, pady=(20, 10))

        # 每 33 毫秒刷新一次影像
        self.after(33, self.update_image)

    def update_tello_image(self):
        # 從攝像頭捕獲影像
        frame = data.cap
        p_frame = data.prossessed_cap
        r_frame = data.recording_cap
        if data.cap is not None:
            # 轉換影像格式並在 GUI 中顯示
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo_image = ImageTk.PhotoImage(image=Image.fromarray(frame))

            p_frame = cv2.cvtColor(p_frame, cv2.COLOR_BGR2RGB)
            p_photo_image = ImageTk.PhotoImage(image=Image.fromarray(p_frame))

            r_frame = cv2.cvtColor(r_frame, cv2.COLOR_BGR2RGB)
            r_photo_image = ImageTk.PhotoImage(image=Image.fromarray(r_frame))
        else:
            pic = Image.open("no_frame.png")
            photo_image = ImageTk.PhotoImage(pic)
        self.image_label3.configure(image=r_photo_image)
        self.image_label3.image = r_photo_image
        self.image_label1.configure(image=photo_image)
        self.image_label1.image = photo_image
        self.image_label2.configure(image=p_photo_image)
        self.image_label2.image = p_photo_image
        # 偷偷放在這
        tt = "state" + data.tello_state + " , battery:" + data.battery + "%"
        self.co.forget()
        self.co = customtkinter.CTkLabel(self.sidebar_frame_left, text=tt,
                                         anchor="s")
        self.co.grid(row=11, column=0, padx=20, pady=(20, 10))

        # 每 33 毫秒刷新一次影像
        self.after(33, self.update_image)

    def another_botton_event(self, id: int):

        if id == 1:  # 錄影
            data.recording = True
            print("tello record")
        elif id == 2:  # 更換模式
            if data.tello_model == "track":
                data.tello_model = "WASD"
                print("tello change model WASD")
            elif data.tello_model == "WASD":
                data.tello_model = "track"
                print("tello change model track")
        elif id == 3:  # 起飛
            data.tello_state = 'stop'
            time.sleep(2)
            self.button2.configure(state="disabled")  # 2
            self.sidebar_button_1.configure(state="disabled")  # 3
            self.sidebar_button_2.configure(state="normal")  # 4
            self.sidebar_button_3.configure(state="normal")  # 5
        elif id == 4:  # 降落
            data.tello_state = 'landed'
            time.sleep(2)
            self.button2.configure(state="normal")  # 2
            self.sidebar_button_1.configure(state="normal")  # 3
            self.sidebar_button_2.configure(state="disabled")  # 4
            self.sidebar_button_3.configure(state="disabled")  # 5
        elif id == 5:  # 暫停/繼續
            if data.tello_state == "tookoff":  # 要暫停
                print("tello stop")
                data.tello_state = 'stop'
                self.button2.configure(state="normal")  # 2
                self.sidebar_button_1.configure(state="disabled")  # 3
                self.sidebar_button_2.configure(state="normal")  # 4

            elif data.tello_state == "stop":  # 要繼續
                print("tello go")
                data.tello_state = 'tookoff'
                self.button2.configure(state="disabled")  # 2
                self.sidebar_button_1.configure(state="disabled")  # 3
                self.sidebar_button_2.configure(state="disabled")  # 4

    def loading_assess(self):
        if data.tello_connected:
            if data.model_activated:
                return "all done!!!"
            else:
                return "activating Mediapipe....."
        else:
            return "connecting Tello....."


if __name__ == "__main__":
    app = App()
    app.mainloop()
