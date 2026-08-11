'''
Googleの「私はロボットではありません。」やCAPTCHA(画像認証)が表示され検索ぺーじからURL取得ができないため、検索までの自動化を実装
'''
# 必要なものをimport
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# ブラウザを開く
options = Options()
driver = webdriver.Chrome(options=options)

# URL設定
url = "https://www.google.com/"

# Googleを開く
driver.get(url)

# 検索ボックスを探して文字を入力して、Enterを押す
search_box = driver.find_element(By.NAME,"q")
search_box.send_keys("Pythonエンジニア")
search_box.send_keys(Keys.RETURN)

# 待機
time.sleep(2)

# ブラウザを閉じる
input("Enterを押すまで閉じません。")
driver.quit()