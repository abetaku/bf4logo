# -*- coding: utf-8 -*-
import os
from random import randint
from PIL import Image, ImageDraw, ImageFont
from mystats import myStats

def pngWithAlpha(filepath, k=1.0):
    # PNG画像の読み込み
    png_img = Image.open(filepath).convert('RGBA')
    png_img.load()
    if k != 1.0 :
        img = png_img.resize( ( int(png_img.size[0] * k), int(png_img.size[1] * k) ) )
    else : 
        img = png_img
    # アルファチャンネルの抽出
    alpha = img.split()[3]
    return img, alpha

def reSizeBg(filepath):
    # 背景の元画像 size -> (0, 0, 992, 345)
    bg_img_orig = Image.open(filepath)
    # 切り取り範囲 (左, 上, 右, 下)
    bgbox = (70, 15, 921, 330)
    # 切り取り
    bg_img = bg_img_orig.crop(bgbox)
    return bg_img

def dgMsg(dr, statsData):
    index = ("NAME  :  %s", "  %s", "TIME   :  %s","KILLS  :  %s", "SPM   :  %s") 
    value = ( statsData['PlayerName'], statsData['RankName'], statsData['TimePlayed'] , statsData['Kills'], statsData['SPM'] )
    fnt = ImageFont.truetype('segoepr.TTF', 10, encoding='utf-8')
    width = 560
    height = 125
    i = 0
    for line in index :
        ext = dr.textsize(line, fnt)
        dr.text((width, height), line % value[i], font=fnt, fill='black')
        height += ext[1] + 7
        i += 1

def bgPickUp(path):
    # 背景用画像をランダムにピックアップ
    files = os.listdir(path)
    filename = files[ randint(0, len(files) - 1 ) ]
    return "%s%s" % (path, filename)
    


if __name__ == '__main__':

    #ランク画像のパスと各種数値を取得
    PARAMS = {'plat':'pc', 'name':'abetaku96', 'opt':'stats,imagePaths,extra,details'}
    client = myStats()
    client.search(mode="playerInfo", parameters=PARAMS)
    client.getStatsData()# 数値は client.statsData に格納されている

     # タイトルの画像
    title_img, title_alpha = pngWithAlpha('./bf4/bf4.png', k=0.4)

    # ランクの画像
    rank_img, rank_alpha = pngWithAlpha(client.statsData['RankImagePath'], k=0.20)

    # 加工用のドッグタグ画像 size -> (0, 0, 256, 128)
    dgtg_img, dgtg_alpha = pngWithAlpha('./bf4/dogtags/advanced0.png', k=1.15)

    # 背景画像 size -> (0, 0, 851, 315)
    bg_img = reSizeBg( bgPickUp("./bf4/maps_large/") )


    # タイトル画像を背景に貼り付け
    bg_img.paste(title_img, (-70,-70), mask=title_alpha)
    # ドッグタグ画像を背景に貼り付け
    bg_img.paste(dgtg_img, (450,95), mask=dgtg_alpha)
    # ランク画像を背景に貼り付け
    bg_img.paste(rank_img, (500, 140), mask=rank_alpha)
    #bg_img.paste(rank_img, (450, 143))
    #bg_img.show()
    #bg_img.save('./result.png')

    # テキストを描画
    dr = ImageDraw.Draw(bg_img)
    dgMsg(dr, client.statsData)
 
    bg_img.show()
