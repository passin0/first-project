# 視覺追蹤無人機

## ✨ 專題程式介紹
這個專案是一個培育「視覺追蹤無人機」的學術研究工程。案例使用 **MediaPipe** 進行物體追蹤，搭配 **DJITello-Python** 控制 Tello 無人機飛行，以及 **OpenCV** 進行影像處理。

## ⚡ 功能簡介
- 目標物的視覺追蹤 (MediaPipe + OpenCV)
- 透過 Wi-Fi 控制 DJI Tello 無人機 (DJITello-Python)
- 將目標物的定位數據作為功能調整依據
- 影像處理並讓機器辨識環境

## ⚖ 機種架構圖
![設計架構圖](設計架構圖.jpg)

## ✈ 開發歷程圖
![開發歷程圖](開發歷程圖.jpg)

## 🛠 安裝方法
使用以下指令安裝所需套件：
```sh
pip install mediapipe opencv-python customtkinter djitellopy
```

## ⚙ 使用步驟
1. 啟動 DJI Tello 無人機並連接 Wi-Fi
2. 執行 Python 程式：
   ```sh
   python main.py
   ```
3. 觀看追蹤效果

## 📊 依賴套件
本專案使用以下開源套件：
- [MediaPipe](https://developers.google.com/mediapipe) - Apache 2.0 License  
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - MIT License  
- [DJITello-Python](https://github.com/dji-sdk/Tello-Python) - MIT License  
- [OpenCV](https://opencv.org/) - Apache 2.0 License  

這些套件的版權屬於其原始開發者，使用時請遵守各自的授權條款。

## ✅ License
本專案使用 **MIT License**，您可以自由使用、修改、分享此代碼，但須保留原始授權註明。



