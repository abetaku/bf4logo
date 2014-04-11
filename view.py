# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
from mystats import myStats

if __name__ == '__main__':
    PARAMS = {'plat':'pc', 'name':'abetaku96', 'opt':'stats,imagePaths,extra,details'}
    client = myStats()
    client.search(mode="playerInfo", parameters=PARAMS)
    client.getStatsData()
    img = Image.open(client.statsData['RankImagePath'])
    img.show()
