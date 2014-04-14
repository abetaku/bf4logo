# -*- coding: utf-8 -*-

#import httplib2
#import json
from pprint import pprint
from bf4api import Bf4StatsApiClient
from datetime import timedelta


class myStats(Bf4StatsApiClient):

    def __init__(self):
        Bf4StatsApiClient.__init__(self)
        self.statsData = {}

    def getStatsData(self):
        self.statsData['TimePlayed'] = self._getTimePlayed()
        self.statsData['SPM'] = self._getSPM()
        self.statsData['RankImagePath'] = self._getRankImagePath()
        self.statsData['RankName'] = self._getRankName()
        self.statsData['Kills'] = self._getKills()
        self.statsData['PlayerName'] = self._getPlayerName()
        return self.statsData
        
    def _getTimePlayed(self):
        dur = self.res['player']['timePlayed']
        return self.__getTimePlayed(dur)

    def __getTimePlayed(self, dur):
        td = timedelta(seconds=int(dur))
        pt = ( (int(td.days)*24+int(td.seconds//3600)),
                 (td.seconds//60)%60,
                 (td.seconds%60) )
        return "%s h %s m %s s" % pt

    def _getSPM(self):
        spm_value = self.res['stats']['extra']['spm']
        return self.__getSPM(spm_value)
    
    def __getSPM(self, spm_value):
        return int(spm_value)

    def _getRankImagePath(self):
        imgPath = "./" + self.res['player']['rank']['imgLarge']
        return imgPath

    def _getRankName(self):
        name = self.res['player']['rank']['name']
        return name

    def _getKills(self):
        kills = self.res['stats']['kills']
        return int(kills)

    def _getPlayerName(self):
        name = self.res['player']['name']
        return name


if __name__ == '__main__':
    PARAMS = {'plat':'pc', 'name':'abetaku96', 'opt':'stats,imagePaths,extra,details'}
    client = myStats()
    client.search(mode="playerInfo", parameters=PARAMS)
    pprint(client.getStatsData())
