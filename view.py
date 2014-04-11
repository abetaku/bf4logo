# -*- coding: utf-8 -*-

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
    index = ("NAME  :  %s", "RANK  :  %s","KILLS  :  %s", "SPM  :  %s", "TIME  :  %s") 
    value = ( statsData['PlayerName'], statsData['RankName'], statsData['Kills'], statsData['SPM'], statsData['TimePlayed'] )
    fnt = ImageFont.truetype('AGENCYB.TTF', 24, encoding='utf-8')
    width = 460
    height = 150
    i = 0
    for line in index :
        ext = dr.textsize(line, fnt)
        dr.text((width, height), line % value[i], font=fnt, fill='green')
        height += ext[1]
        i += 1



if __name__ == '__main__':

    #ランク画像のパスと各種数値を取得
    PARAMS = {'plat':'pc', 'name':'abetaku96', 'opt':'stats,imagePaths,extra,details'}
    client = myStats()
    client.search(mode="playerInfo", parameters=PARAMS)
    client.getStatsData()# 数値は client.statsData に格納されている

    # ランクの画像
    rank_img, rank_alpha = pngWithAlpha(client.statsData['RankImagePath'], k=0.25)

    # 加工用のドッグタグ画像 size -> (0, 0, 256, 128)
    dgtg_img, dgtg_alpha = pngWithAlpha('./bf4/dogtags/advanced0.png', k=1.1)

    # 背景画像 size -> (0, 0, 851, 315)
    bg_img = reSizeBg("./bf4/maps_large/mp_naval.jpg")

    # ドッグタグ画像を背景に貼り付け
    bg_img.paste(dgtg_img, (400,100), mask=dgtg_alpha)
    # ランク画像を背景に貼り付け
    bg_img.paste(rank_img, (380, 100), mask=rank_alpha)
    #bg_img.show()
    #bg_img.save('./result.png')

    # テキストを描画
    dr = ImageDraw.Draw(bg_img)
    dgMsg(dr, client.statsData)
 
    bg_img.show()
