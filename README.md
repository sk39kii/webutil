# webutil
PythonでWebアクセスユーティリティ

## 概要
スクレイピングする時によく使う処理をまとめました。  
基本動作として、Requestsでアクセスして取得したhtmlをBeautifulSoupでパースします。

## 使用方法

### 前準備

requestsとbeautifulsoup4をpipでインストールします。

```sh
pip install requests
pip install beautifulsoup4
```

### インポート

ログ出力したいスクリプトで以下のようにインポートする。

```py
# Webアクセスユーティリティクラス
from webutil import WebUtil
```

### 使い方

#### 文字コードを指定する

アクセスするWebサイトの文字コードを指定します。  

```py
def __init__(self):
    # Webサイトの文字コードを指定
    self.SITE_ENCODE = 'cp932'
```

#### GETリクエストする

指定したURLにアクセスしコンテンツの内容をBeautifulSoupのオブジェクトに変換します。  
後は要素を指定することで値が取得できます。
```py
wu = WebUtil()
doc = wu.parse_bs4('https://www.python.org/')
site_title = doc.find('title').string
print site_title

Welcome to Python.org
```

リクエストを投げる際に何もしていしなければGETメソッドでリクエストします。

#### POSTリクエストする

POSTメソッドでリクエストしたい場合は以下のようにします。
```py
## POST Request
payload = {'post_form_data_name': 'value'}
doc = wu.parse_bs4(url, 'POST', payload)
```

#### アクセス間隔について

連続してアクセスしないようにアクセス前にスリープします。 

スリープする時間を変更したい場合は以下を書き換えてください。  
※FAKE_ACCESS_MIN(秒)　〜　FAKE_ACCESS_MAX(秒)の間でランダムな時間スリープします。  
```py
def __init__(self):
    # スリープの最小時間(秒)
    self.FAKE_ACCESS_MIN = 3
    # スリープの最大時間(秒)
    self.FAKE_ACCESS_MAX = 10
```

スリープ自体をやめたい場合は以下を書き換えてください。  
※FAKE_ACCESSをTrueからFalseにする  
```py
def __init__(self):
    # True:アクセス前にランダムな時間スリープする
    self.FAKE_ACCESS = True
```

> ※連続してアクエスしすぎると相手のWebサーバ管理者に迷惑がかかります。  
>  場合によっては不正アクセスとみなされる場合もありますので、  
>  間隔をあけてアクセスすることをおすすめします。  

#### ユーザエージェントを書き換える

ユーザエージェントを書き換える場合は以下を変更します。

```py
def __init__(self):
    self.USERAGENT = '{0:s}{1:s}'.format(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ',
        '(KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'')'')'
    )
```

#### エンコードについて

Webサイトのエンコードがsjis系の場合は、取得したコンテンツを無条件にCP932でエンコードしています。  

BeautifulSoupでパースする時にエンコードしたい場合は以下をTrueに変更します。

```py
def __init__(self):
    # True:BeautifulSoupでパースする時にエンコードをかける
    self.BS4_ENCODEFLG = False
```

#### 単純にアクセスだけする

値は取得せずにただアクセスしたい場合はget_contentでアクセスします。

```py
wu.get_content(url)
```


## 課題・検討

- todo:特定の要素の中から文字列のみを取得する時に余計な空白を除去する
- todo:単純なアクセスするときのメソッドがget_contentだが何もgetしてないのでメソッドの名前を変更
- todo:設定の変更用のメソッドを作成する
