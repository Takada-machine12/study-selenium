# ブラウザを自動操作するためseleniumをimport
from selenium import webdriver
# seleniumでEnterキーを送信する際に使用するのでimport
from selenium.webdriver.common.keys import Keys
# seleniumでブラウザの検索テキストボックスの属性を取得するためにimport
from selenium.webdriver.common.by import By
# Google Chromeのドライバーを管理・起動するためにimport
from selenium.webdriver.chrome.service import Service as ChromeService
# seleniumでヘッドレスモード(裏で動作させるモード)を指定するためにimport
from selenium.webdriver.chrome.options import Options
# 待ち時間を指定するためにtime(プログラムを一時停止したりするのに使用)をimport
import time
# 正規表現にマッチする文字列を探すためにreをimport
import re
# エラー内容の詳細を表示するためにimport
import traceback

# Googleのトップページ
URL = "https://www.google.com"

def main():
    '''
    メインの処理
    Googleの検索エンジンでキーワードを検索
    指定されたドメインが検索結果の１ページ目に含まれていないキーワードをテキストファイルに出力
    '''

    # '検索キーワードリスト.txt'ファイルを読み込み、リストにする
    with open('転職キーワードリスト.txt') as f:
        keywords = [s.rstrip() for s in f.readlines()] # 1行ずつ取り出して、改行除去してsに入れた後、keywordsに入れる

    # 'ドメインリスト.txt'ファイルを読み込み、リストにする
    with open('ドメインリスト.txt') as f:
        domains = [s.rstrip() for s in f.readlines()] # １行ずつ読み込んで改行コードを削除してリストにする

    # seleniumで自動操作するブラウザはGoogleChrome
    # Optionsオブジェクトを作成
    options = Options()
    # ヘッドレスモードを有効にする(ブラウザが立ち上がった時に見えない形で裏で動作させる)
    # options.add_argument('--headless')

    # ChromeのWebDriverオブジェクトを作成
    # Chormeブラウザを起動させて、Pythonで操作できるようにする
    service = ChromeService()
    driver = webdriver.Chrome(service=service, options=options)

    # Googleのトップページを開く
    driver.get(URL)
    # 2秒待機（読み込みのため）
    time.sleep(2)

    # 指定ドメインに含まれていないならキーワードをok_keywordlistに追加
    ok_keywordlist = []

    # 検索キーワードを1つずつ取り出す
    for keyword in keywords:
        # search関数実行
        search(keyword, driver)
        # get_url関数を実行し、戻り値をurlsに代入
        urls = get_url(driver)
        # domain_checked関数を実行し、戻り値をweak_ok_keywordlistに代入
        weak_ok_keywordlist = domain_checked(urls, domains, ok_keywordlist, keyword)

    # '結果.txt'という名前を付けて、ドメインチェックしたキーワードをファイルに書き込む
    # ドメインチェック済みのキーワードを１行ずつ保存
    with open('結果.txt', 'w') as f:
        f.write('\n'.join(weak_ok_keywordlist))

    # ブラウザを閉じる
    driver.quit()

def search(keyword, driver):
    '''
    検索テキストボックスに検索キーワードを入力し、検索する
    '''

    # 検索テキストボックスの要素をname属性から取得
    input_element = driver.find_element(By.NAME,"q")
    # 検索テキストボックスに入力されている文字列を消去
    input_element.clear()
    # 検索テキストボックスにキーワードを入力
    input_element.send_keys(keyword)
    # Enterキーを送信
    input_element.send_keys(Keys.RETURN)
    # 2秒待機
    time.sleep(2)
    # タイトルにキーワードが含まれていることを確認

def get_url(driver):
    '''
    検索結果ページの1位から10位までのURLを取得
    '''

    # 各ページのURLを入れるために空のリストを用意
    urls = []
    # a要素（各ページの1位から10位までのURL）取得
    objects = driver.find_elements(By.CSS_SELECTOR, "#search a")
    #tsuid_n-p6aqH2LcDX1e8P6ZOF0AE_41 > div > div:nth-child(2) > div:nth-child(3) > div > div > div > div > div > div.v5yQqb > a

    # a要素の取得有無で処理を分ける
    if objects:
        for object in objects:
            urls.append(object.get_attribute("href"))
    else:
        print("URLを取得できませんでした。")
    # 各ページのURLを戻り値に指定
    return urls


def domain_checked(urls, domains, ok_keywordlist, keyword):
    '''
    URLリストからドメインを取得し、指定ドメインに含まれているかチェック
    '''
    # 取得・保存したURLリストから各ページのURLを１つずつ取り出す
    for url in urls:
        m = re.search(r'//(.*?)/', url) # '//〇〇/'に一致する箇所（ドメイン）を抜き出す
        domain = m.group(1)            # '//〇〇/'の'〇〇'に一致する箇所を抜き出し、domainに代入
        
        if 'www.' in domain:            # ドメインに'www.'が含まれているかチェック
            domain = domain[4:]         # 含まれているなら'www.'を除去
        if domain in domains:           # 各ページのドメインが指定ドメイン(ドメインリスト.txt)に含まれているかチェック
            # 整形したキーワードが大手キーワードに含まれているなら警告を出す
            print(f"キーワード「{keyword}」の検索結果には大手ドメインがありましたので除外します。")
            break                       # １つでも含まれているなら他はチェックする必要がないので関数を終了
    else:                               # 大手キーワードではないキーワードであれば、リストに保存
        ok_keywordlist.append(keyword)
    # ドメインチェック済みのキーワードを戻り値に指定
    return ok_keywordlist

# main関数を実行
try:
    # このファイルが直接実行された時のみ実行させる
    if __name__ == '__main__':
        main()
except Exception as e:
    print(f"エラー内容：{e}")
    traceback.print_exc()
input("Enterを押すまでChromeを開いたままにします...")