#!/usr/bin/env python

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
