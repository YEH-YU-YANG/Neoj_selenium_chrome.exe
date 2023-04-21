# Neoj爬蟲,模擬人類複製貼上

連接不了 $Neoj$ 能夠看到學生 $code$ 的 $API$，總是 response<500> 。
只能採用腳本刷新 $challenge$ 頁面，並複製 $code$，貼上到本地檔案內，在用 $standford moss$ 比對抄襲。

這個方法是笨、慢、負擔很大，期望未來有講師成功串起 $API$，或開發出更厲害的腳本。

環境 : windows64/ python3.9.6 / chrome 112.0.5615....

**2023/4/22更新:結果學弟馬上把API串起來......**

## 執行過程
![](https://i.imgur.com/1jg9LBA.gif)


## 使用方法

### Chrome.exe

先進說明中心查看本地端google版本

![](https://i.imgur.com/dpbOsd8.png)

![](https://i.imgur.com/L4DNkHA.png)

得知google版本後，到[這裡](https://chromedriver.chromium.org/)下載對應版本和 OS 的 chrome.exe
selenium會使用這個chrome.exe開啟網站，注意chrome.exe版本要抓對喔~，不然會閃退。

### selenium 登入 neoj

```cpp!
user_email.clear()
user_password.clear()
user_email.send_keys('')  # 放入自己的帳號(mail)
user_password.send_keys('')  # 放入自己的密碼
login_button.click() 
```

### pyautogui抓滑鼠左壓起始點
![](https://i.imgur.com/M6DfFyk.png)

![](https://i.imgur.com/yTC5vbm.jpg)

截圖左上角，如圖。
把這張圖片放```{pwd}/{date}/{problem_id}```之下，e.g. ```Desktop/py/project/0308/289```

滑鼠會偵測這張截圖的中心點，後續程式會把滑鼠下拉到code黑框的第一行，因此**截圖時一定要截到code黑框第一行的一半**，後續程式會把滑鼠用這張圖中心座標的y值的兩倍，下拉到那個地點，這樣會剛好拉到code第一行。

```cpp
# 找反白起始點
# 圖片必須用neoj左上角往右下拉到code黑框的第一條
# 圖片路徑要根據自己檔案的位置配置
# 這邊是放在 pwd\imgs\date\ 之下,圖片名稱是problem_id,檔案.jpg
start_position = pyautogui.locateCenterOnScreen(r"{}\imgs\{}\{}.jpg".format(os.getcwd(),date,pid),confidence=0.9) 
while start_position is None:
	start_position = pyautogui.locateCenterOnScreen(r"{}t\imgs\{}\{}.jpg".format(os.getcwd(),date,pid),confidence=0.9) 

# 反白
time.sleep(0.5)
pyautogui.mouseDown(20,2*start_position.y+5,button='left') # 滑鼠左鍵壓著
time.sleep(0.5)
pyautogui.moveTo(5,pyautogui.size().height-2) # 滑鼠左鍵壓著下拉
time.sleep(1) # 若1秒內下拉不完頁面，必須加長時間，保證反白到全部的code
pyautogui.moveTo(pyautogui.size().width-40,pyautogui.size().height-80,) #滑鼠左鍵壓著右拉
pyautogui.mouseUp(pyautogui.size().width-40,pyautogui.size().height-80,button='left')
# time.sleep(0.2)

```

**注意圖片路徑要調入自己電腦上的路徑**

### 學生Database

```cpp!
user_list = [3856,4028,4001,3999,3853,3964,3236,3893,3848,3880,4026,3965,3996,3994,3855,4029,3849,3867,3874,3962,3881,3981,4008,4018,3997,3986,4009,3899,3883,3995,3234,3974,3847,4106,3872,3892,3862,4019,3851,3854,3879,3976,3985,3958,3959,3852,4027,3980,3978,4030,3871,3998,3967,3465,3864,3897,4070,3957,4007,3972,3979,3876,3877,3861,3859,4010,4006,3898,3993,3984,3884,4016,3878,3887,3860,4002]

problem_list = {
    'deadline' : '20230318',
    'pid' : [451,645,764,893]
}
```
```user_list```是學生neoj上的id
```problem_list['deadline']``` 第i週作業的deadline
```problem_list['pid']``` 第i週作業的題號

一次能抓一週的份量。
要抓特定學生就改```user_list```
要抓特定題目就改```problem_list['pid']```
