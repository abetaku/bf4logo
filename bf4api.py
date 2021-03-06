
# -*- coding: utf-8 -*-

#import sys
import httplib2
import json
from pprint import pprint


class Bf4StatsApiClient(object):

    def __init__(self):
        # REST API のエンドポイント
        self._endpoint = "http://api.bf4stats.com/api/"
        # 初期化用のエンドポイント
        self._init = "http://bf4stats.com/"
        # モード
        self._mode = { 
                              "onlinePlayers":"onlinePlayers",
                              "playerInfo":"playerInfo", 
                              "playerRankings":"playerRankings"
                            }
        # 表現のフォーマット
        self._format = "json"
        # 直近のリクエストURI
        self.last_uri = ""
        # 直近のレスポンス
        self.res={}

    def search(self, mode, parameters={}):
        # リクエストのクエリパラメータ
        request_query = parameters
        request_query["output"] = self._format
        return self._search(mode, request_query)

    def _search(self, mode,  query):
        # 辞書型のクエリパラメータを文字列に変換する
        query_str = "&".join(['%s=%s' % (key, value) for key, value, in query.items()])
        # リクエストする URI を作る
        request_uri = "%s%s?%s" % (self._endpoint, self._mode[mode], query_str)
        self.last_uri = request_uri
        # BF4STATSの初期化用　URI
        if 'plat' in query and 'name' in query:
            init_uri = "%s%s/%s" % (self._init, query['plat'], query['name'])
            pass
        else :
            init_uri = None
            pass
        return self._request(request_uri, init_uri)

    def _request(self, uri, init):
        # HTTP クライアントを得る
        http_client = httplib2.Http(".cache")
        # REST API を呼び出す
        if init is not None :
            r, c = http_client.request(init, "GET") # データ初期化
            pass
        resp, content = http_client.request(uri, "GET")
        return self._deserialize(content)

    def _deserialize(self, content):
        # レスポンスの JSON を Python オブジェクトに変換する
        self.res = json.loads(content.decode('utf-8'))
        return self.res


if __name__ == '__main__':
    client = Bf4StatsApiClient()
    response_entity = client.search(mode="onlinePlayers")
    pprint(response_entity)
