# -*- coding: utf-8 -*-

import socket
import string
import urllib2
import time
import json
import random
from time import sleep

#Acc
HOST = "irc.twitch.tv"
NICK = "BotName"
PORT = 6667
PASS = "oauth:" + ""
readbuffer = ""
MODT = False

oplist = {}
namechannel = "Channel name"

def connect(host, port):
    s = socket.socket()
    s.connect((host, port))
    return s

def joinChannel(s, channel):
    s.send("JOIN #" + channel + " \r\n")

def auth(s, passwd):
    s.send("PASS " + passwd + "\r\n")

def setNickname(s, nickname):
    s.send("NICK " + nickname + "\r\n")

def isop(user):
    return user in oplist

ch = 0
coolch = "КРУТО!"
i = 0
fort = 0


sock = connect(HOST, PORT)
auth(sock, PASS)
setNickname(sock, NICK)
joinChannel(sock, namechannel)

def Send_message(message):
    sock.send("PRIVMSG #" + namechannel + " :" + message + "\r\n")

url = "http://tmi.twitch.tv/group/user/" + namechannel + "/chatters"
req = urllib2.Request(url, headers={"accept": "*/*"})
res = urllib2.urlopen(req).read()



def viewerlist():
    viewerlist = ""
    try:
        if res.find("502 bad gateway") == - 1:
            oplist.clear()
            data = json.loads(res)
            for p in data["chatters"]["viewers"]:
                oplist[p] = "viewer"

            for p in oplist:
                if oplist[p] == "viewer":
                    viewerlist += p + ", "

    except:
        "Error.."
    return viewerlist


def modslist():
    modslist = ""
    try:
        if res.find("502 bad gateway") == - 1:
            oplist.clear()
            data = json.loads(res)
            for p in data["chatters"]["moderators"]:
                oplist[p] = "mod"

            for p in oplist:
                if oplist[p] == "mod":
                    modslist += p + ", "

    except:
        "Error.."
    return modslist



while True:
    bufferSize = 1024
    data = sock.recv(bufferSize)
    readbuffer += data
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()

    if len(data.rstrip()) == 0:
        print('Connection was lost, reconnecting')
        sock.close()
        sock = connect(HOST, PORT)
        auth(sock, PASS)
        setNickname(sock, NICK)
        joinChannel(sock, namechannel)

    for line in temp:

        if (line[0] == "PING"):
            sock.send("PONG %s\r\n" % line[1])
        else:

            parts = string.split(line, ":")

            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                try:

                    message = parts[2][:len(parts[2]) - 1]
                except:
                    message = ""

                usernamesplit = string.split(parts[1], "!")
                username = usernamesplit[0]

                if MODT:
                    print username + ": " + message

                    ########################################
                    ##########------COMMANDS-------#########
                    ########################################

                    if message == ("!хей"):
                        Send_message("Добро пожаловать, " + username)

                    if message == "!timeout":
                        Send_message("/timeout " + username + " 30")

                    if message == "!uptime":
                        uptime = urllib2.urlopen("https://decapi.me/twitch/uptime?channel=" + namechannel).read()
                        Send_message(uptime)

                    if message == "!time":
                        Send_message(time.strftime("%I:%M %p %Z on %A %B %d %Y"))

                    if message == "!myicq":
                        random.seed(username)
                        Send_message(username + ", you icq = " + str(random.randint(1, 210)))

                    if message == ("mods"):
                        Send_message(modslist())

                    if message == ("!а может ли бот написать симфонию?"):
                        Send_message("Симфония")

                    if message == ("!true_noirhat"):
                        Send_message("God!")

                    if message == ("!pidor"):
                        random.seed(username)
                        Send_message(username + " - пидор на " + str(random.randint(0, 100)) + "%")
                        
                    if message == ("!mymmr"):
                        random.seed(username)
                        pts = random.randint(1, 9500)
                        if pts > 7000:
                            Send_message(username + " you mmr = " + str(pts) + " PogChamp")
                        if pts < 2500:
                            Send_message(username + " you mmr = " + str(pts) + " SMOrc ")
                        else:
                            Send_message(username + " you mmr = " + str(pts))

                    if message == ("!камень"):
                        random.seed()
                        igr = random.randint(1, 3)
                        if igr == 1:
                            Send_message("камень! Ничья!")
                        if igr == 2:
                            Send_message("ножницы! Я проиграл!")
                        if igr == 3:
                            Send_message("бумага! Ты проиграл!")
                            Send_message("/timeout " + username + " 10")

                    if message == ("!ножницы"):
                        random.seed()
                        igr = random.randint(1, 3)
                        if igr == 1:
                            Send_message("камень! Ты проиграл")
                        if igr == 2:
                            Send_message("ножницы! Ничья")
                        if igr == 3:
                            Send_message("бумага! Я проиграл")
                            Send_message("/timeout " + username + " 10")

                    if message == ("!бумага"):
                        random.seed()
                        igr = random.randint(1, 3)
                        if igr == 1:
                            Send_message("камень! Я проиграл")
                        if igr == 2:
                            Send_message("ножницы! Ты проиграл")
                            Send_message("/timeout " + username + " 10")
                        if igr == 3:
                            Send_message("бумага! Ничья")

                    if message == ("!срань"):
                        Send_message("https://github.com/Winetricks/winetricks/blob/master/src/winetricks")

                    if message == ("off-qqwwq") and isop(username):
                        exit()

                    if message == ("!commands"):
                        Send_message("!хей, !timeout, !uptime, !time, !myicq, !pidor, !mymmr, !камень, !ножницы, !бумага, !commands")

                    if message == "ЧЕЧНЯ":
                        Send_message(coolch)
                        ch +=1
                        if ch >= 10:
                            coolch = "ЛУЧШАЯ!"

                    if message == "ЧЕЧЕНЯ":
                        Send_message(coolch)

                    if message == "!СУПЕРЧЕЧНЯ":
                        while i < 6:
                            i+=1
                            Send_message("ЧЕЧНЯ - " + coolch)

                    if message == "АЛЛАХ":
                        Send_message("КРУТО")

                    if message == "Саймон":
                        Send_message("Верстальщик срани")

                    if message == "казахи":
                        Send_message("Сверхлюди")
                    
                    if message == "!bot":
                        Send_message("https://github.com/TheToka/TheTokaBot-twitch-bot")
                        
                    if message == "!форт":
                        fort += 1
                        Send_message("Прогресс: " + str(fort) + "%")
                        if fort == 100:
                            Send_message("Прогресс: 100%, вы закончили форт")
                            fort = 0

                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True
