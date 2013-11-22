#!/usr/bin/env python
#
# Copyright 2012-2013 ihptru (Igor Popov)
#
# This file is part of cei_stats, which is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

cmds = ""
ladderlog = ""

class Winzone:
    def __init__(self, cmds, ladderlog):
        self.cmds = cmds
        self.ladderlog = ladderlog

    def flush(self, data):
        file = open(self.cmds, 'a')
        file.write(data)
        file.close()
    
    def show(self):
        while 1:
            line = sys.stdin.readline()
            line = line.rstrip()
            line_args = line.split(' ')
            if line_args[0] == 'PLAYER_ENTERED':
                player = line_args[1]
                data = open(self.ladderlog, 'r').readlines()
                player_stats = {}
                block = 0
                for item in data:
                    item = item.split()
                    if item[0] == "WINZONE_PLAYER_ENTER":
                        if block == 0:
                            player_stats[item[4]] = player_stats.get(item[4], 0) + 1
                            block = 1
                    else:
                        block = 0
                sorted_winners = sorted(player_stats.items(), key=lambda t: t[1])
                sorted_winners.reverse()
                self.flush("PLAYER_MESSAGE \""+player+"\" \"0xffff00Those who escaped (top 20):\"\n")
                for i in range(len(sorted_winners)):
                    if i==10: break
                    try:
                        msg = "PLAYER_MESSAGE \""+player+"\" \""+("0x00ff00"+(sorted_winners[i][0]+":").ljust(25)+"0xffffff"+str(sorted_winners[i][1])).ljust(50)+"0x00ff00"+(sorted_winners[i+10][0]+":").ljust(25)+"0xffffff"+str(sorted_winners[i+10][1])+"\"\n"
                    except:
                        msg = "PLAYER_MESSAGE \""+player+"\" \"0x00ff00"+(sorted_winners[i][0]+":").ljust(25)+"0xffffff"+str(sorted_winners[i][1])+"\"\n"
                    self.flush(msg)

if __name__ == "__main__":
    winzone = Winzone(cmds, ladderlog)
    winzone.show()
