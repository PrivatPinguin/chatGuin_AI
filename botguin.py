import discord
import random
import re
import json
from discord.channel import VoiceChannel
from datetime import datetime
import requests
from datetime import datetime
import chat
import cred

client = discord.Client()

def getData(key):
    print('todo') #getData

openweathermap = '__openweathermap_API_key__'
nasaString = '__nasaString_API_key__'

guildID = 12345678901234567890 # your guild id
otherBotID = 12345678901234567890 # if you have an ohter bot
userVoiceLog_ChannelID = 12345678901234567890 # id of log channel
firstBotID = 12345678901234567890 # your 1st bot id
secondBotID = 12345678901234567890 # your 2nd bot id
whatUserDo = 12345678901234567890 # ID of a random user
channel_Spam_talk = 12345678901234567890 # id of spam channel
channel_AI_talk = 12345678901234567890 # id of AI talk channel
admin_ID = 12345678901234567890 # your ID


def saveLog(logText):
    f = open("F:\Programme\python\discordBot\chatInhalte.log", "a")
    f.write(logText + '\n')
    f.close()
    print('{}\n'.format(logText))

@client.event
async def on_ready():
    print('STARTING\tUsername: {}'.format(client.user.name))
    print('\t   \tClient ID: {}\tREADY'.format(client.user.id))

async def splitMSG(message):
    if len(message)<2000:
        await message.channel.send(message)
    else:
        n = 2000
        for i in range(0, len(message), n): 
            await message.channel.send(message[i:i+n])
    
# def writeChatLog(logText):
    # logTxt = ('INFO\t{}\t{}\t{}\t{} {}'.format(datetime.now(),ctx.message.author.id, authorName, order, logText))
    # saveLog(logTxt)

# def writeLog(order, logText):
    # authorName = ctx.message.author.name.encode()
    # logTxt = ('INFO\t{}\t{}\t{}\t{} {}'.format(datetime.now(),ctx.message.author.id, authorName, order, logText))
    # saveLog(logTxt)
def cntWhitespace(arg):
    count=0
    for i in arg:
        if(i.isspace()):
            count=count+1
    return count

def regexError():
    return ('>>> \n\ntry:\n\tFind:[   **$regex**   **f**(Argument)   **regex**(String)   **Text**(String)   ]\nor\n\tReplacet:[   **$regex**   **r**(Argument)   **regex**(String)   **replace**(String)   **Text**(String)   ]')


def regex(arg): # $regex r foo baa fofoofofofofofofoo foo fofoofofoofofofoofofooofofo
    #writeLog('$regex', arg)
    if arg:
        arg = arg.split(' ', 1)
        op = arg[0] # 'r' 'c' 'f' 
        result = ''
        if op=='r':
            if cntWhitespace(arg[1])>2:
                arg = arg[1].split(' ', 2)
                regex = arg[0]
                subst = arg[1]
                test_String = arg[2]
                ctr = 0
                result = re.sub(regex, subst, test_String, 0, re.MULTILINE)

                if result:
                    result = '**Resultat**: ```{}```'.format(result)
                else:
                    result = '>>> Regex Replace Error ¯\_(ツ)_/¯\n\nNO RESULT' + regexError()
            else:
                result = '>>> Missing Strings ¯\_(ツ)_/¯\n\nNO RESULT' + regexError()
        else:
            if op == 'f':
                if arg[1]:
                    arg = arg[1].split(' ', 1)
                    regex = arg[0]
                    test_String = arg[1]
                    matches = re.finditer(regex, test_String, re.MULTILINE)
                    result='```'
                    for matchNum, match in enumerate(matches, start=1):
                        result +=  'Match {matchNum} was found at {start}-{end}: {match}\n'.format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group())
                        for groupNum in range(0, len(match.groups())):
                            groupNum = groupNum + 1
                            result += 'Group {groupNum} found at {start}-{end}: {group}\n'.format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum))
                    result +='```'
                    if not result:
                        result = '>>> Regex Error ¯\_(ツ)_/¯\n\nNO RESULT' + regexError()   
            else:
                result = '>>> Argument Error ¯\_(ツ)_/¯\n\nNO RESULT' + regexError()
    return result

async def getMoreWetterData(message,city):
    data = requests.get('http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&lang=de'.format(city,openweathermap))
    data = json.loads(data.text)
    inCelsius = -273.15
    city = data['city']['name']
    wetterText = '```Wetter in {}```'.format(city)
    vorherigesDatum = ''
    for wetter in data['list']:
        if len(wetterText)<1800:
            description = ''
            datum = wetter['dt_txt']
            if (vorherigesDatum[0:10] != datum[0:10]) and (datum[11:19] == '12:00:00'):
                vorherigesDatum = wetter['dt_txt']
                temperature = round(wetter['main']['temp']+ inCelsius)
                min = round(wetter['main']['temp_min']+ inCelsius)
                max =  round(wetter['main']['temp_max']+ inCelsius)
                temperature_feel_like = round(wetter['main']['feels_like']+ inCelsius)
                for s in wetter['weather']:
                    description += s['description']
                speed = wetter['wind']['speed']
                humidity = wetter['main']['humidity']
                datum = wetter['dt_txt']
                wetterText += ('```Datum: {}```\n Tempeatur: {} °C\n {} gefühlt: {}°C\nWind: {}m/s\n Luftfeuchtigkeit: {}%\n Im Verlauf: {}°C bis {}°C\n\n'.format(datum, temperature, description, temperature_feel_like, speed, humidity, min, max))
        else:
            await message.channel.send(wetterText)
            wetterText = ''
    return wetterText

def getWetterData(data):
    inCelsius = -273.15
    description = ''
    city = data['name']
    temperature = round(data['main']['temp']+ inCelsius)
    min = round(data['main']['temp_min']+ inCelsius)
    max =  round(data['main']['temp_max']+ inCelsius)
    temperature_feel_like = round(data['main']['feels_like']+ inCelsius)
    for s in data['weather']:
        description += s['description']
    speed = data['wind']['speed']
    humidity = data['main']['humidity']
    return ('>>> Die Temperatur in **{}** beträgt **{} °C**,\n es ist **{}** und fühlt sich wie **{} °C** an,\n der Wind ist **{} m/s** schnell und es gibt eine Luftfeuchtigkeit von **{} %**\n Temperaturen zwischen **{} °C** und **{} °C** sind zu erwarten.'.format(city, temperature, description, temperature_feel_like, speed, humidity, min, max))


def wetterPri(arg):
    data = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=de'.format(arg, openweathermap))
    data = json.loads(data.text)
    return getWetterData(data)


def ipLocate(arg):
    data = requests.get('https://freegeoip.app/json/{}'.format(arg))
    data = json.loads(data.text)
    ip = data['ip']
    country_code = data['country_code']
    country_name = data['country_name']
    region_code = data['region_code']
    region_name = data['region_name']
    city = data['city']
    zip_code = data['zip_code']
    time_zone = data['time_zone']
    latitude = data['latitude']
    longitude = data['longitude']
    metro_code = data['metro_code']
    return ('>>> **IP INFO:**\n\nIP: **{}**\n country_code: **{}**\n country_name: **{}**\n region_code: **{}**\n region_name: **{}**\n city: **{}**\n zip_code: **{}**\n time_zone: **{}**\n latitude: **{}**\n longitude: **{}**\n metro_code: **{}**\n'.format(ip, country_code, country_name, region_code, region_name, city, zip_code, time_zone, latitude, longitude, metro_code))

@client.event
async def on_voice_state_update(member, before, after):
    for guild in client.guilds:
        if guild.id == guildID:
            channel = client.get_channel(userVoiceLog_ChannelID)
            for thisChannel in guild.channels:                         
                try:
                    if after.channel.id:
                        if after.channel.id == thisChannel.id:
                            datetimeNow = str(datetime.now())
                            datetimeNow = datetimeNow[0:19]
                            await channel.send('>>> INFO:\t **JOIN**\nDT:\t{}\nMember:\t{}\nChannel:\t{}'.format(datetimeNow, member, after.channel))  
                except:
                    if before.channel.id:
                        if before.channel.id == thisChannel.id:
                            datetimeNow = str(datetime.now())
                            datetimeNow = datetimeNow[0:19]
                            await channel.send('>>> INFO:\t **LEAVE**\nDT:\t{}\nMember:\t{}\nChannel:\t{}'.format(datetimeNow, member, before.channel))  

def replaceUmlaute(msg):
    msg = msg.replace("ue","ü")
    msg = msg.replace("oe","ö")
    msg = msg.replace("ae","ä")
    msg = msg.replace("Ue","Ü")
    msg = msg.replace("Oe","Ö")
    msg = msg.replace("Ae","Ä")
    msg = msg.replace("sz","ß")
    #msg = msg.replace("Ü","Ue")
    #msg = msg.replace("Ö","Oe")
    #msg = msg.replace("Ä","Ae")
    return msg

def reverse(thisBool):
    return not thisBool
    
#toTest
def kiFunctions(msg):
    functions = ['$_Boring', '$_Keyword01']
    if any(msg in functions):
        for word in functions:
            if word == '$_Boring':
                data = requests.get('https://www.boredapi.com/api/activity')
                data = json.loads(data.text)
                return ('>>> **You should:** {}'.format(data['activity']))
            elif word == '$_Keyword01':
                print('\n\nINFO:\tkeyword 01 detected')

def kiTalk(message):
    msg = chat.say(message)
    msg = replaceUmlaute(msg)
    return msg

callBotguin = 0
activeKi = False
@client.event
async def on_message(message):
    if message.author == client.user:
        print('\n\n___SELF_MSG:\n\n')
        print('guild\t{}'.format(message.guild))
        print('channel\t{}'.format(message.channel))
        print('content\t{}'.format(message.content))
        print('\nI am, who I am...\n')
        return 0
    if ((message.author.id != firstBotID) and (message.author.id != secondBotID)):
        saveLog(message.clean_content)
    if message.author != client.user:
        for guild in client.guilds:
            if message.guild.id == guildID: 
                for thisChannel in guild.channels:
                    if thisChannel.id == channel_AI_talk: #ki-talk - textchat
                        msg = kiTalk(message)
                        await message.channel.send(msg)
                        return 0
                    if thisChannel.id == channel_Spam_talk: #spam - textchat
                        if message.clean_content == '$ki':
                            global activeKi
                            activeKi = reverse(activeKi)
                            if activeKi:
                                await message.channel.send('Lass uns reden. ☜(ﾟヮﾟ☜)')
                                return 0
                            else:
                                await message.channel.send('Schon gut, ich bin leise.. ༼ つ ◕_◕ ༽つ')
                                return 0
                        elif activeKi:
                            msg = kiTalk(message)
                            await message.channel.send(msg)
                            # msg = replaceUmlaute(message)
                            # msg = chat.say(msg)
                             #chat.py import
    if message.author.id == whatUserDo: #just a user
        wtfMsg = ['was soll das? Was tust du da?:', 'dein ernst?', 'toll gemacht.']
        msg = random.choice(wtfMsg)
        await message.channel.send('>>> @{}, {}'.format(message.author,msg))
        return 0
    if message.author.id == otherBotID:
        print('\n\n________NEW_MSG:\n\n')
        print('guild\t{}'.format(message.guild))
        print('channel\t{}'.format(message.channel))
        print('content\t{}'.format(message.content))
        print('\nmet:Bot2105')        
        if message.content.startswith('>>> **You should:**'):
            await message.channel.send('>>> I would like to do this, too!')
        else:
            global callBotguin 
            if callBotguin<5:
                callBotguin += 1
                await message.channel.send('>>> Hallo @{}'.format(message.author))
            else:
                callBotguin = 0
                await message.channel.send('>>> Warum antwortet @{} mir nicht? (╯°□°）╯︵ ┻━┻'.format(message.author))                
        return 0
     
        """ some on_message command """
    else:
        print()
        print(message.author.id)
        print()
        print('\n\n________NEW_MSG:\n\n')
        print('guild\t{}'.format(message.guild))
        print('channel\t{}'.format(message.channel))
        print('author\t{}'.format(message.author))
        print('content\t{}'.format(message.content))
        print('\nEND_OF_MSG\n\n')
        original_msg = message.content
        msg_content = message.content.lower()
        # delete curse word if match with the list
        if message.guild.id == "__guildID__":
            curseWord = ['http:', 'https:', 'www.']              
            if not ((message.channel.id == "__fistChannelID__") or (message.channel.id == "__secondChannelID__")):
                if any(word in msg_content for word in curseWord):
                    for word in curseWord:
                        original_msg = regex('r {} ***** {}'.format(word,original_msg))
                    try:
                        await message.edit(original_msg)
                    except:
                        print('cant edit')
                        await message.delete() #replace with #* : send
                    await message.channel.send('>>> Hey {}, bitte keine Links auf diesem Discord senden.'.format(message.author))  
                    return 0
    if message.author.id == admin_ID:
        if message.content.lower().startswith('prognose'):
            print(message.content)
            message.content = message.content.replace("prognose","$prognose")
            await message.channel.send('>>> Versuche es mit:')
            await message.channel.send('>>> {}'.format(message.content))
            return 0
        
        # if message.content.startswith('$ip'):
            # args = message.content
            # args = args.replace("$ip ","")
            # await message.channel.send(ipLocate(args))
        #was geht?
        # if re.search('was\sgeht.*', message.content.lower()):
            # await message.channel.send('>>> Ich bin ein Bot, ich mache wozu ich geschaffen wurde!')
            # return 0
        #wie ist das wetter?
        if re.search('(().*(w(eath|ett|at)er)\sin\s)', message.content.lower()):
            city = re.sub('(().*(w(eath|ett|at)er)\sin\s)', '', message.content.lower())
            city = re.sub('\s.*', '', city)          
            await message.channel.send(wetterPri(city))
        #track södkjslökjf sjf sdfsj  8.8.8.8 sfalhgjksdhlasjhlgjksh
        if re.search('(\d{1,3}\.){3}(\d{1,3})', message.content):
            ipString = re.sub('[^((\d{1,3}\.){3}(\d{1,3}))]', '', message.content)
            txt = ipLocate(ipString)
            await message.channel.send(txt)
        ##bot joins voice
        # if message.content.lower().startswith('hierher'):
            # channel = message.author.voice.channel
            # print(message.author.voice)
            # print(message.author.voice.channel)
            # await channel.connect()
            # await message.channel.send('>>> Bin da.')
        # else:
            # if message.content.lower().startswith('raus'):
                #print(client.user.voice_client)
                # print(client)
                # print(client.user)
                # channel = message.author.voice.channel
                # print(channel)
                #await channel.disconnect(client.user.voice_client)
                # await channel.disconnect()
                
                #await client.message.author.voice.disconnect()
                # await message.channel.send('>>> Bis bald.')



# @client.command()
# async def join(ctx):
    # channel = ctx.author.voice.channel
    # await channel.connect()
    
# @client.command()
# async def leave(ctx):
    # await ctx.voice_client.disconnect()


client.run(cred.getCred('BOTAPIKEY'))