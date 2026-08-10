# ブラウザを自動操作するためseleniumをimport
from selenium import webdriver
# seleniumでEnterキーを送信する際に使用するのでimport
from selenium.webdriver.common.keys import Keys
# seleniumでブラウザの検索テキストボックスの属性を取得するためにimport
from selenium.webdriver.common.by import By
# seleniumでヘッドレスモード(裏で動作させるモード)を指定するためにimport
from selenium.webdriver.chrome.options import Options
# 待ち時間を指定するためにtime(プログラムを一時停止したりするのに使用)をimport
import time
# 正規表現にマッチする文字列を探すためにreをimport
import re

# Googleのトップページ
URL = "https://www.google.com"
'''
メインの処理
Googleの検索エンジンでキーワードを検索
指定されたドメインが検索結果の１ページ目に含まれていないキーワードをテキストファイルに出力
'''

# '検索キーワードリスト.txt'ファイルを読み込み、リストにする
with open('転職キーワードリスト.txt') as f:
    keywords = [s.rstrip() for s in f.readlines()] # 1行ずつ取り出して、改行除去してsに入れた後、keywordsに入れる
print(keywords)
# 'ドメインリスト.txt'ファイルを読み込み、リストにする
with open('ドメインリスト.txt') as f:
    domains = [s.rstrip() for s in f.readlines()]
print(domains)
# １行ずつ読み込んで改行コードを削除してリストにする

# seleniumで自動操作するブラウザはGoogleChrome
# Optionsオブジェクトを作成
options = Options()
# ヘッドレスモードを有効にする(ブラウザが立ち上がった時に見えない形で裏で動作させる)
# options.add_argument('--headless')

# ChromeのWebDriverオブジェクトを作成

# Chormeブラウザを起動させて、Pythonで操作できるようにする
driver = webdriver.Chrome(options=options)

# Googleのトップページを開く
driver.get(URL)
# 2秒待機（読み込みのため）

# 検索キーワードを１つずつ取り出す
# search関数実行
# get_url関数を実行し、戻り値をurlsに代入
# domain_checked関数を実行し、戻り値をok_keywordlistに代入

# '結果.txt'という名前を付けて、ドメインチェックしたキーワードをファイルに書き込む

# ドメインチェック済みのキーワードを１行ずつ保存

# ブラウザーを閉じる

'''
検索テキストボックスに検索キーワードを入力し、検索する
'''

# 検索テキストボックスの要素をname属性から取得
input_element = driver.find_element(By.NAME,"q")
# 検索テキストボックスに入力されている文字列を消去
input_element.clear()
# 検索テキストボックスにキーワードを入力
input_element.send_keys("転職")
# Enterキーを送信
input_element.send_keys(Keys.RETURN)
# 2秒待機
time.sleep(2)
'''
検索結果ページの1位から10位までのURLを取得
'''

# 各ページのURLを入れるために空のリストを用意
urls = []
# a要素（各ページの1位から10位までのURL）取得
objects = driver.find_elements(By.TAG_NAME, "a")
# rso > div:nth-child(7) > div > div > div > div.kb0PBd.A9Y9g.jGGQ5e > div > div > span > a

# a要素の取得有無で処理を分ける
if objects:
    for object in objects:
        urls.append(object.get_attribute("href"))
else:
    print("URLを取得できませんでした。")
# 各ページのURLを戻り値に指定

'''
URLリストからドメインを取得し、指定ドメインに含まれているかチェック
'''
# URLリストから各ページのURLを１つずつ取り出す

# '//〇〇/'に一致する箇所（ドメイン）を抜き出す
# '//〇〇/'の'〇〇'に一致する箇所を抜き出し、domainに代入
# ドメインに'www.'が含まれているかチェック
# 含まれているなら'www.'を除去
# 各ページのドメインが指定ドメインに含まれているかチェック
# 含まれているなら警告を出す
# １つでも含まれているなら他はチェックする必要がないので関数を終了
# 指定ドメインに含まれていないならキーワードをok_keywordlistに追加
# ドメインチェック済みのキーワードを戻り値に指定

# main関数を実行

input("Enterを押すまでChromeを開いたままにします...")
driver.quit()