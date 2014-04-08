# -*- coding: utf-8 -*-

import sys
import httplib2
import json




class Bf4StatsApiClient(object):

    def __init__(self):
        # REST API のエンドポイント
        self._endpoint = "http://api.bf4stats.com/api/"
        # モード
        self._mode = {"onlinePlayers":"onlinePlayers", "playerInfo":"playerInfo", "playerRankings", "playerRankings"}
        # 表現のフォーマット
        self._format = "json"

    def search(self, mode, **parameters):
        # リクエストのクエリパラメータ
        request_query = parameters
        request_query["output"] = self._format
        return self._search(mode, request_query)

    def _search(self, mode,  query):
        # 辞書型のクエリパラメータを文字列に変換する
        query_str = reduce(lambda s, (k, v): \
                           "%s&%s=%s" % (s, k, v), query.iteritems(), "")
        # リクエストする URI を作る
        request_uri = "%s%s?%s" % (self._endpoint, self._mode[mode], query_str[1:])
        return self._request(request_uri)

    def _request(self, uri):
        # HTTP クライアントを得る
        http_client = httplib2.Http(".cache")
        # REST API を呼び出す
        resp, content = http_client.request(uri, "GET")
        return self._deserialize(content)

    def _deserialize(self, content):
        # レスポンスの JSON を Python オブジェクトに変換する
        return json.loads(content)

if __name__ == '__main__':
    client = Bf4StatsApiClient()
    response_entity = client.search(sys.argv[1], sys.argv[2])
    print response_entity
