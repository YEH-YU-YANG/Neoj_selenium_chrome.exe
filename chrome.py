from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
import os
import pyautogui
import keyboard
import pyperclip
import info_obj


# 導向neoj登入頁面
option = webdriver.ChromeOptions()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)
driver.maximize_window()
login_url = 'https://neoj.sprout.tw/ingress/'
driver.get(login_url)

# 抓取輸入欄位
user_email = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id=\"ingress\"]/div[2]/form/div[1]/div/div[2]/input"))
)
user_password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id=\"ingress\"]/div[2]/form/div[2]/div/div[2]/input"))
)
login_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id=\"ingress\"]/div[2]/form/div[3]/div/div[1]/button"))
)
# 輸入欄位
user_email.clear()
user_password.clear()
user_email.send_keys('') # 放入自己的帳號(mail)
user_password.send_keys('')  # 放入自己的密碼
login_button.click() 
time.sleep(1)

'''
# 把軟體開發自動執行的bar關掉
auto_input_position = pyautogui.locateCenterOnScreen(r"D:\py\project\imgs\auto_input.jpg",confidence=0.9)
while auto_input_position is None:
    auto_input_position = pyautogui.locateCenterOnScreen(r"D:\py\project\imgs\auto_input.jpg",confidence=0.9)
pyautogui.moveTo(auto_input_position)
for i in range(0,30):
    print(f'...Initialize... {i} times...')
    pyautogui.moveTo(auto_input_position.x,auto_input_position.y+i)
    pyautogui.click()
time.sleep(1)

# 刷新頁面，讓bar消失
# driver.refresh()
'''


# 爬蟲
challenge_prefix_url = 'https://neoj.sprout.tw/challenge/'
info_list = info_obj.info_list

i=0;
length = len(info_list)

for data in info_list:

    sid = str(data['student_id'])
    pid = str(data['problem_id'])
    date = str(data['start_day'])
    challenge_id = str(data['challenge'])
    
    challenge_url = challenge_prefix_url + str(challenge_id)
    driver.get(challenge_url)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id=\"challenge\"]/div[1]/div[1]/button"))
    )
    
    pyautogui.FAILSAFE = False
    
    # 找反白起始點
    # 圖片必須用neoj左上角往右下拉到code黑框的第一條
    # 圖片路徑要根據自己檔案的位置配置 img_path = "D:\py\project\imgs\{}\{}.jpg".format(date,pid)
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

    # 複製
    keyboard.press('ctrl')
    keyboard.press('c')
    keyboard.release('c')
    keyboard.release('ctrl')
    time.sleep(0.2)

    # 建立資料夾
    folder_name = '{}\{}'.format(date,pid)
    folder_path = os.path.join(os.getcwd(), folder_name)  # 使用os.getcwd()取得當前路徑
    os.makedirs(folder_path, exist_ok=True)
    if not os.path.exists(folder_path):
        print(f"Directory {folder_name} is built in {folder_path}")

    # 在資料夾中寫入檔案
    file_name = challenge_id + ".cpp"
    file_path = os.path.join(folder_path, file_name)
    paste_file = pyperclip.paste()
    text = "\n".join([line for line in paste_file.splitlines() if line.strip()])
    with open(file_path, "w",encoding='UTF-8') as file:
        try:
            file.write(text)  
            i += 1
            print(f"FILE {file_name} is created under the path: {file_path} , remaining {length-i} data.")
        except:
            print("Problem: {pid}, Student:{sid}, challengr:{challenge_id} , error between writing file.")
    
    
    # time.sleep(1)
    
print("Mission complete")
