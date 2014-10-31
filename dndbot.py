#!/usr/bin/env python
# -*- coding: utf-8 -*-
import vk
import random
import time
import mechanize
import sys
import codecs
from collections import deque

class player:
  def __init__(self, uid, playername, statlist = None, charname = ''):
    self.id = uid
    self.name = playername
    self.char = charname
    if (statlist == None):
      self.statl = {'STR': 10, 'DEX':10, 'CON':10, 'WIS':10, 'INT':10, 'CHA':10}
    else:
      self.statl = statlist

  stats = {'STR','DEX','CON','WIS','INT','CHA'}
  def modifier(self, stat):
    return (int(self.statl[stat]) - 10) / 2

  def setstat(self,stat,newvalue):
    self.statl[stat] = newvalue

  def getstat(self,stat):
    return self.statl[stat]

  def getinfo(self):
    res = self.name + "\n"
    res += "Character: " + unicode(self.char) + "\n"
    for s in ['STR','DEX','CON','INT','WIS','CHA']:
      res += s + ": " + str(self.getstat(s)) + " (modifier: " + str(self.modifier(s)) + ")\n"
    return res

class vkBot:
  def __init__(self, token):
    
    self.vkapi = vk.API(access_token=token, timeout = 10)
    self.messages_answered = deque(maxlen=20) #чтобы не отвечать на уже обработанные сообщения #TODO: запоминание при выходе
    self.players = {}
    self.players_ids = list()
    self.gamemaster = ""


  stats = {'STR','DEX','CON','WIS','INT','CHA'}
  
  def str_to_stat(self, name): #TODO: русские названия
    name = name.upper()
    if (name in ('STR','STRENGTH')):
      return 'STR'
    if (name in ('DEX','DEXTERITY')):
      return 'DEX'
    if (name in ('CON','CONSTITUTION')):
      return 'CON'
    if (name in ('WIS','WISDOM')):
      return 'WIS'
    if (name in ('INT','INTELLIGENCE')):
      return 'INT'
    if (name in ('CHA','CHARISMA')):
      return 'CHA'
    return name
	
  def get_messages(self, first_time = False):
    messages = self.vkapi.messages.get()['items'] + self.vkapi.messages.get(out = "1")['items'] 
    for message in messages:
      message_body = message['body']
      message_sender_id = str(message['user_id'])
      message_id = message['id']
      m_chat_id = message['chat_id'] if 'chat_id' in message.keys() else ''
      res = ""
      if ((message_body == 'test') and (not (message_id in self.messages_answered))):
        print message_body
        res = self.testtest()
        print res

      if ((message_body.startswith('!roll')) and (not (message_id in self.messages_answered))):
        print message_body
        res = self.roll(message_sender_id,message_body)
        print res

      if ((message_body.startswith('!set')) and (not (message_id in self.messages_answered))):
        print message_body
        res = self.set_stat(message_sender_id,message_body)
        print res

      if ((message_body.startswith('!get')) and (not (message_id in self.messages_answered))):
        print message_body
        words = msg.Body.split()
        if (len(words) > 2):
          res = self.get_stat(words[1],words[2])
        else:
          if (len(words) == 2):
            res = self.get_stat(message_sender_id,words[1])
          else:
            res = "What are you trying to get?"
        print res
      if ((message_body.startswith('!info')) and (not (message_id in self.messages_answered))):
        print message_body
        words = message_body.split()
        if (len(words) > 1):
          res = self.players[words[1]].getinfo()
        else:
          res = self.players[message_sender_id].getinfo()
      if (res != ""):
        if (not first_time):
          if (m_chat_id != ''):
            self.vkapi.messages.send(chat_id = m_chat_id, message = res)
          else:
            self.vkapi.messages.send(user_id = message_sender_id, message = res)
        self.messages_answered.append(message_id)

  def get_fullname(self, uid):
    profile = self.vkapi.users.get(user_id=str(uid))[0]
    return profile["first_name"]+" "+profile["last_name"]
    
  
  def add_player(self, playerid, statlist = None, charname = ""):
    self.players[playerid] = player(playerid, self.get_fullname(playerid), statlist, charname)
    self.players_ids.append(playerid)

  def add_players(self, fname):
    try:
      f = codecs.open(fname, "r", "utf-8")
      self.gamemaster = f.readline()
      print "Gamemaster: " + self.gamemaster
      print "Players: "
      for line in f:
        args = line.split()
        print args
        if (len(args) == 8):
          self.add_player(args[0], {'STR':args[2], 'DEX':args[3], 'CON':args[4], 'WIS':args[5], 'INT':args[6], 'CHA':args[7]}, args[1])
        else:
          if (len(args) == 7):
            self.add_player(args[0], {'STR':args[1], 'DEX':args[2], 'CON':args[3], 'WIS':args[4], 'INT':args[5], 'CHA':args[6]})
          else:
            if (len(args) == 2):
              self.add_player(args[0], {'STR':10, 'DEX':10, 'CON':10, 'WIS':10, 'INT':10, 'CHA':10}, args[1])
            else:
              self.add_player(args[0])
      #print self.players
    except:
      print "Problems with opening/reading a file. Processing without it."

  def roll_dice(self, nmb, pool, mod = 0):
    thrown = list()
    res = mod
    for i in range(nmb):
      newr = random.randint(1,pool)
      thrown.append(newr)
      res += newr
    return (res,thrown)

  def set_stat(self, uid, command): #TODO: запоминание при выходе
    words = command.split()
    if (uid == self.gamemaster):
      name = words[1] #В результате ГМ может устанавливать статы только по id игрока. Плохо. TODO: сделать доступ по имени персонажа или еще чему-то
      stat = self.str_to_stat(words[2])
      value = int(words[3])
    else:
      name = uid
      stat = self.str_to_stat(words[1])
      value = int(words[2])
    self.players[name].setstat(stat,value)
    return self.players[name].char + '\'s ' + stat + ' set to ' + str(value)

  def get_stat(self, name, stat):
    return self.players[name].char + "\'s " + stat + " is " + str(self.players[name].getstat(self.str_to_stat(stat))) + " (modifier " + str(self.players[name].modifier(self.str_to_stat(stat))) + ")."

  def parse_dice(self, dstr):
    #Вообще все это regexp-ами делается, но мне так лень с ними разбираться... (TODO: разобраться и сделать)
    if (dstr == ""): #!roll = !roll 1d20
      return (1,20,0)
    words = dstr.split()
    if (len(words) == 2): #!roll a b
      return (int(words[0]), int(words[1]), 0)
    if (len(words) > 2): #!roll a b c
      return (int(words[0]), int(words[1]), int(words[2]))
    #!roll <number>d<pool>([+/-]<mod>)
    nmbs = dstr.partition('d')[0]
    dstr = dstr.partition('d')[2]
    nmb = int(nmbs) if (nmbs != "") else 1
    mod = 0
    mods = dstr.partition('+')[2]
    mod = int(mods) if (mods != "") else mod
    mods = '-'+dstr.partition('-')[2]
    mod = int(mods) if (mods != "-") else mod
    
    pool = int((dstr.split("+")[0]).split("-")[0])
    return (nmb,pool,mod)

  def parse_stat_dice(self, uid, statstr):
    statstrs = statstr.split('+')
    nmb = 1
    pool = 20
    mod = 0
    if (not (uid in self.players_ids)):
      player = player(uid)
    else:
      player = self.players[uid]
    for s in statstrs:
      if (self.str_to_stat(s) in self.stats):
        mod += player.modifier(self.str_to_stat(s))
    return (nmb, pool, mod)
  
  def roll(self, uid, dicestr):
    words = dicestr.split()

    if ((len(words) > 1) and (not words[1][0].isdigit())): #rolling stats
      nmb, pool, mod = self.parse_stat_dice(uid,words[1])
      if (len(words) > 2):
        mod += int(words[2])
    else:
      nmb, pool, mod = self.parse_dice(dicestr.partition(" ")[2])

    res, thrown = self.roll_dice(nmb,pool,mod)
    
    res_str = self.get_fullname(uid) + ' rolled ' + str(nmb) + " of d" + str(pool) + " dice with modifier " + str(mod) + ".\nDice thrown:"
    for d in thrown:
        res_str += ' ' + str(d)

    res_str += '\nResult = '
    res_str += str(res)
    return res_str


  def testtest(self):
      return "test successfull"
		
app_id = "4607475"
		
if __name__ == "__main__":
  if (len(sys.argv) >= 2):
    username = sys.argv[1]
    password = sys.argv[2]
    print "connecting, please wait"
    br = mechanize.Browser()
    br.open('https://oauth.vk.com/authorize?client_id='+app_id+'&scope=4098&redirect_uri=http://oauth.vk.com/blank.html&display=wap&response_type=token')

    br.select_form(nr=0)
    br.form['email'] = username
    br.form['pass'] = password
    br.submit()
    try:
            br.select_form(nr=0)
            br.submit()
    except:
            pass
    redirect_url = br.geturl()
    token = redirect_url.split('token=')[1].split('&')[0]
  else:
    url = 'https://oauth.vk.com/authorize?client_id='+app_id+'&scope=4098&redirect_uri=http://oauth.vk.com/blank.html&display=wap&response_type=token'
    print "It's okay for you not to trust me your email and password. Still, I need an access to your account to recieve/send messages. So please, go to " + url + ", give me permissions I ask for and give me access token you see in the url you're redirected to"
    token = raw_input("access_token = ")
  
  bot = vkBot(token)
  print "connected"

  filename = raw_input("You can also specify a file from which I should take information about players (I will search for \"players.txt\" by default)")
  if (filename == ""):
    filename = "players.txt"
  bot.add_players(filename)
  print "Ready to recieve queries"
  time.sleep(3.0)
  bot.get_messages(True)
  while True:
    time.sleep(3.0)
    bot.get_messages()
    
