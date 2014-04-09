# -*- coding: utf-8 -*-

import httplib2
import json
from pprint import pprint
from bf4api import Bf4StatsApiClient
from datetime import timedelta
from PIL import Image, ImageDraw

class AbtkStats(Bf4StatsApiClient):
        
    def getTimePlayed(self):
        dur = self.res['player']['timePlayed']
        return self._getTimePlayed(dur)

    def _getTimePlayed(self, dur):
        td = timedelta(seconds=int(dur))
        pt = ( (int(td.days)*24+int(td.seconds//3600)),
                 (td.seconds//60)%60,
                 (td.seconds%60) )
        return "%sh%sm%ss" % pt

    def getSPM(self):
        spm_value = self.res['stats']['extra']['spm']
        return self._getSPM(spm_value)
    
    def _getSPM(self, spm_value):
        return int(spm_value)

    def getRankImagePath(self):
        imgPath = "./" + self.res['player']['rank']['imgLarge']
        return imgPath

if __name__ == '__main__':
    PARAMS = {'plat':'pc', 'name':'abetaku96', 'opt':'stats,imagePaths,extra'}
    client = AbtkStats()
    client.search(mode="playerInfo", parameters=PARAMS)
    #pprint(client.res)
    #print(client.getTimePlayed())
    #print(client.getSPM())
    img = Image.open(client.getRankImagePath())
    img.show()

    # デフォルト背景色の 128x128 サイズのキャンヴァスを用意する。
    #img = Image.new('RGBA', (128, 128))

    # Draw 関数でオブジェクトを作成。
    #draw = ImageDraw.Draw(img)

    # 画面の左上隅にテキストを赤く描画する。
    #draw.text((0, 0), u'Hello, world', fill='red')

    #img.save("test.gif")
