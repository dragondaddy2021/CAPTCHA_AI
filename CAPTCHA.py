# 需要用到的模組導入區
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import warnings
from selenium.webdriver import ActionChains 
from selenium.webdriver.common.keys import Keys
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
from io import BytesIO
import base64
import cv2
import numpy as np

#警告：《文化創意產業發展法》已針對濫用AI模組有相關規範和罰則，本件程式碼已進行去識別化並刪減內容，僅供教學概念使用，切莫以身試法。

#import cv2、import numpy as np之前要先在終端機安裝pip install opencv-python、pip install numpy

# 去除不建議使用的醜醜警告
warnings.filterwarnings("ignore", category=DeprecationWarning)

# 設定 Chrome 瀏覽器的執行檔路徑， r"..." 來指定 ChromeDriver 路徑，這可以確保程式碼中的反斜線（\）被當作字元而非跳脫字元處理。
chrome_driver_path = r"Chrome 瀏覽器的執行檔路徑"

# 啟動 Chrome 瀏覽器
browser = webdriver.Chrome(executable_path=chrome_driver_path)

# 最大化瀏覽器視窗
browser.maximize_window()

# 前往網站URL
browser.get("網站URL")

"""
以下為自動化測試用例
"""
print("以下為自動化測試用例結果")

# 強制等待5秒渲染頁面
time.sleep(5)

# 驗證碼辨識後輸入流程，目前測試此段流程處理後之圖片可以成功辨識出文字，但因目前成功機率較低，須另外訓練Tesseract模型，因此暫時先將此段註解起來，
# 待未來有空訓練模型後再行使用，以下為成功的圖片預處理和辨識機制。

# 請先安裝Tesseract程式包之後再使用終端機操作pip安裝pytesseract及圖像處理套件：pip install pytesseract、pip install pillow
# C槽使用者路徑下的AppData\Local\Programs\Tesseract-OCR\tesseract.exe要記得加入到系統的環境變數

time.sleep(2)

# 先將頁面截圖保存起來
browser.save_screenshot("XXX.png")

captcha_icon = browser.find_element(By.ID, 'ID本人')
left = captcha_icon.location['x'] + 160
top = captcha_icon.location['y'] + 60
right = left + captcha_icon.size['width'] + 50
bottom = top + captcha_icon.size['height'] + 10
im = Image.open('XXX.png')
im = im.crop((left, top, right, bottom))
im.save('captcha.png')

pytesseract.pytesseract.tesseract_cmd = r"C槽使用者路徑下的AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# 將圖片轉為灰階圖像
im = Image.open('captcha.png')
im = im.convert('L')  
im.save('captcha.png')
im.show()

# 二值化處理
im = im.point(lambda x: 0 if x < 160 else 255)  
im.save('captcha.png')
im.show()

'''
# 使用中值濾波器進行模糊處理(看情況使用)
im = Image.open('captcha.png')
im = im.filter(ImageFilter.MedianFilter(size=5))
im.save('captcha.png')
im.show()
'''

# 增加圖像對比度
im = Image.open('captcha.png')
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(1.5)
im.save('captcha.png')
im.show()

'''
# 進行邊緣檢測處理(看情況使用)
im = im.filter(ImageFilter.FIND_EDGES)
im.save('captcha.png')
im.show()

# 進行高斯模糊處理(看情況使用)
im = im.filter(ImageFilter.GaussianBlur(radius=1))
im.save('captcha.png')
im.show()
'''

# 將圖片調整為300x100的大小
im = Image.open('captcha.png')
im = im.resize((300, 100))  
im.save('captcha.png')
im.show()

'''
# 設置識別區域(看情況使用)
im = Image.open('captcha.png')
width, height = im.size
im = im.crop((0, 0, width, height/2))
im.save('captcha.png')
im.show()
'''

# 進行OCR識別
captcha_text = pytesseract.image_to_string(im, lang='eng', config='--psm 6')

print(captcha_text)

# 定位驗證碼輸入欄位
captcha_input = browser.find_element(By.ID, 'ID本人')

# 透過行為鍊的方式先移動到驗證碼輸入框點擊之後再輸入驗證碼後送出
ActionChains(browser).move_to_element(captcha_input).click(captcha_input).send_keys(captcha_text).perform()

#等待5秒確認結果
time.sleep(5)
