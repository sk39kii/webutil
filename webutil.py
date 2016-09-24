#! /usr/bin/env python
# -*- coding: utf-8 -*-

u"""Web Access Utility Class

pip install requests
pip install beautifulsoup4
"""

from bs4 import BeautifulSoup
import json
import random
import requests
import sys
import time


class WebUtil(object):
    u"""Webアクセスユーティリティクラス"""

    def __init__(self):
        # 疑似アクセスフラグ
        # True:アクセス前にランダムな時間スリープする
        self.FAKE_ACCESS = True
        # スリープの最小時間(秒)
        self.FAKE_ACCESS_MIN = 3
        # スリープの最大時間(秒)
        self.FAKE_ACCESS_MAX = 10
        # Webサイトの文字コードを指定
        self.SITE_ENCODE = 'cp932'
        # エンコードフラグ
        # True:BeautifulSoupでパースする時にエンコードをかける
        self.BS4_ENCODEFLG = False
        self.USERAGENT = '{0:s}{1:s}'.format(
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ',
            '(KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'')'')'
        )

    def _check_random_sleep(self):
        u"""ランダムな時間スリープするかチェック"""
        if self.FAKE_ACCESS and self.FAKE_ACCESS_MAX > 0:
            self.random_sleep(self.FAKE_ACCESS_MIN, self.FAKE_ACCESS_MAX)

    def random_sleep(self, startsec, endsec):
        u"""ランダムな時間スリープする
        startsec: 最小ランダム時間(秒)
        endsec:   最大ランダム時間(秒)
        """
        sleepsec = random.randint(startsec, endsec)
        self.nomal_sleep(sleepsec)

    def nomal_sleep(self, sleepsec):
        u"""ただのスリープ
        sleepsec: スリープする時間(秒)
        """
        time.sleep(sleepsec)

    def _get_params(self, limit, args):
        u"""可変長パラメータの取得
        limit: 必要なパラメータの個数
        *args: パラメータ(可変長)のリスト
        """
        ret = []
        # リストから必要な分だけ取得。個数が足りない場合はNoneで埋める
        for i, val in enumerate(args):
            ret.append(val)
            if len(ret) == limit:
                break
        while len(ret) < limit:
            ret.append(None)
        # 必要な個数が2個以上だと多値返却になるが
        # 1個だとリストとして返却される為、1個の場合は値を返す
        if limit == 1:
            return ret[0]
        return ret

    def _init_request(self, url):
        u"""リクエスト準備
        url: リクエストするURL
        """
        headers = {'User-Agent': self.USERAGENT}
        timeoutsec = 20
        urlverify = True if url.startswith('https') else False
        return (headers, timeoutsec, urlverify)

    def post(self, *args):
        u"""WebサイトにPOSTリクエスト
        *args: 可変長リスト[URL, Dictionary of POST data]
        """
        url, payload = self._get_params(2, args)
        headers, timeoutsec, urlverify = self._init_request(url)
        self._check_random_sleep()
        # セッションを開始してPOST
        s = requests.session()
        r = s.post(
            url,
            data=payload,
            headers=headers,
            timeout=timeoutsec,
            verify=urlverify)

        # サイトのエンコードがsjis系の場合は、取得したコンテンツをCP932でエンコード
        e = r.encoding.lower()
        if e.find('windows') > -1 \
           or e.find('jis') > -1 \
           or e.find('cp932') > -1:
            r.encoding = 'cp932'

        # エンコードをセットして返却
        result = ''
        result = r.text.encode(r.encoding)
        return result

    def access(self, *args):
        u"""WebサイトにGETリクエストをする
        URLにGETパラメータは既に付いている前提
        *args: 可変長リスト[URL]
        """
        url = self._get_params(1, args)
        headers, timeoutsec, urlverify = self._init_request(url)
        self._check_random_sleep()
        # セッションを開始してアクセス
        s = requests.session()
        r = s.get(
            url,
            headers=headers,
            timeout=timeoutsec,
            verify=urlverify)

        # サイトのエンコードがsjis系の場合は、取得したコンテンツをCP932でエンコード
        e = r.encoding.lower()
        if e.find('windows') > -1 \
           or e.find('jis') > -1 \
           or e.find('cp932') > -1:
            r.encoding = 'cp932'

        # エンコードをセットして返却
        result = ''
        result = r.text.encode(r.encoding)
        return result

    def get_content(self, *args):
        u"""サイトにGETアクセスしhtmlを取得
        *args: 可変長リスト[URL]
        """
        return self.access(*args)

    def parse_bs4(self, *args):
        u"""サイトにアクセスしhtmlをパースしdomを返す(bs4)
        *args: 可変長リスト[URL, 'POST', Dictionary of POST data]
        1:URL           ※必須
        2:'GET'or'POST' ※POSTリクエスト時は必須
        3:Post Data     ※POSTリクエスト時は必須
        """
        url, method, payload = self._get_params(3, args)
        if method == 'POST':
            html = self.post(url, payload)
        else:
            html = self.access(*args)

        if self.BS4_ENCODEFLG:
            return BeautifulSoup(html, 'html.parser',
                                 from_encoding=self.SITE_ENCODE)
        else:
            return BeautifulSoup(html, 'html.parser')

    def safe_str_encode(self, value, trim=True):
        u"""対象の文字列から不要な文字の変換・除去した後エンコードして返却
        value: 対象の文字列
        trim:  True:左右についている空白文字と改行を除去する
        """
        return self.safe_str(value, trim).encode(self.SITE_ENCODE)

    def safe_str(self, value, trim=True):
        u"""対象の文字列から不要な文字の変換・除去し返却
        value: 対象の文字列
        trim:  True:左右についている空白文字と改行を除去する
        """
        # nbsp(ノンブロッキングスペース=ユニコードスペース)を変換
        # LinuxでCtrl+<space> Alt+<space>
        wk = value.replace(u'\xa0', ' ')

        # 全角コーテーションを除去
        wk = self.clear_char(wk)
        # 前後の空白、改行文字を除去
        if trim:
            wk = wk.strip()
            # 先頭の「=」を「-」に変換
        return self.first_replace(wk, '=', '-')

    def clear_char(self, val):
        u"""対象の文字列から不要な文字を削除"""
        if isinstance(val, unicode):
            val = val.replace(u'“', '')
            val = val.replace(u'”', '')
        elif isinstance(val, str):
            val = val.replace(u'“'.encode('cp932'), '')
            val = val.replace(u'”'.encode('cp932'), '')
        return val

    def first_replace(self, val, f, t):
        u"""文字列の先頭文字が特定の文字の場合に置換する
        val: 対象の文字列
        f:   特定の文字
        t:   変換する文字
        """
        repstr = val
        if val.startswith(f):
            repstr = val.replace(f, t, 1)
        return repstr


def main():
    u"""exsample"""
    wu = WebUtil()
    doc = wu.parse_bs4('https://www.python.org/')
    site_title = doc.find('title').string
    print site_title

    # POST Request
    # payload = {'post_form_data_name': 'value'}
    # doc = wu.parse_bs4(url, 'POST', payload)

if __name__ == '__main__':
    main()
