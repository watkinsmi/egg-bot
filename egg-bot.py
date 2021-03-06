# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
from discord import Embed
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import random
from egg_assets import greet_txt, tulku_memes, bw_text, fortune_list
import eggscript as es
import re
import bf
import praw
import os.path
import pickle
import subprocess
import eggshells as shells

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Egg Bot", command_prefix="egg-", pm_help = False)


reddit = None
# If you want reddit copypastas, comment line above, uncomment and fill out line below...
# reddit = {'client_id': 'FlwVsmOnx-WwhA', 'client_secret': 'CLIENT_SECRET_HERE', 'user_agent': 'USER_AGENT_HERE', 'test': 'test'}

r = None
if reddit:
    r = praw.Reddit(client_id=reddit['client_id'], client_secret=reddit['client_secret'], user_agent=reddit['user_agent'])

if r:
    if os.path.isfile('./comments'):
        posts = pickle.load(open('./comments', 'rb'))
    else:
        sub = r.subreddit('copypasta')
        posts = list(sub.hot(limit=5000))
        posts = [post.id for post in posts if len(post.selftext) <= 4096]
        pickle.dump(posts, open('./comments', 'wb'))

def create_random_comparison():
    num1 = random.sample(range(1,20), 1)
    num2 = random.sample(range(1,20), 1)
    return num1, num2

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	return await client.change_presence(game=discord.Game(name='Making long eggs: Type egg-greet for more info.')) #This is buggy, let us know if it doesn't work.


#easy test for eggcasting
@client.command()
async def test(*args):

	await client.say("This is a test of my eggcasting system.")
	await asyncio.sleep(3)
	await client.say("Your command was most eggcellent!")

#lists users
@client.command()
async def users(*args):
    list_of_users = []
    users_online = client.get_all_members()
    for member in users_online:
        list_of_users.append(member.name)
    await client.say("There are " + str(len(list_of_users)) + " users inhabiting egg server: " + str(list_of_users))
  
    
#very randomly gives positive reinforcement to chat user
#also has an easter egg.
@client.event
async def on_message(message):
    if str(message.content) == 'I am an eggboy!':
        await client.send_message(message.channel, 'https://youtu.be/yavYMMpzBrA?t=1m21s')
        await client.send_message(message.channel, 'most......EGGSCELLENT!')
    elif str(message.content).lower() == 'goodbye egg bot':
        await client.send_message(message.channel, 'Good night sweet prince...')
    elif str(message.content).lower() == 'hello':
        await client.send_message(message.channel, '''Hello egg boy!
                                                      Welcome to egg channel!
                                                      Home of the egg boys!
                                                      May I be your overlord?''')
    elif str(message.content).lower() == 'yes':
        await client.send_message(message.channel, 'Take down ye trowsers boy!')
    # early implementation of eggscript
    elif (str(message.content).startswith('eggfuck:')):
        await bf.evaluate(message.content[3:].strip(), client, message.channel)
    elif (str(message.content).startswith('eggscript')):
        script = ''
        for line in str(message.content).splitlines():
            if (line.startswith('eggscript')):
                continue
            script += line
        await es.go(script, client, message.channel)
    elif (str(message.content).startswith('eggshells:')):
        await shells.go(str(message.content)[10:], client, message.channel)
    elif str(message.author.name) != 'Egg Bot':
        # I Think This *should* Return Any Question Asked In The Channel In Jeggden Smith Case 10% of the time
        if str(message.content).endswith('?'):
            rnd = random.randint(0, 101)
            print(rnd)
            if rnd > 90:
                msg = transform_msg(' '.join([s[0].upper() + s[1:] for s in str(message.content).split(' ')]))
                await client.send_message(message.channel, 'J🥚den 🔨 Smith ☝ wants 🥈 to 🎓 know: ' + msg)
        else:
            n1, n2 = create_random_comparison()
            if random.randint(0, 101) > 15:
                #await client.send_message(message.channel, 'Eggcellent communication my dude!')
                # rnd = random.randint(0, 26)
                # alpha = 'abcdefghijklmnopqrstuvwxyz'
                m = str(message.content).replace('"', "'")
                # If you want "AI" response, train an OpenNMT-py model and add add the command below, uncommenting the with block:
                # subprocess.check_output(f'echo "{m}" > ./m.txt && python ./ai/OpenNMT-py/translate.py -model ./ai/orlando_ai_model_step_30000.pt -src ./m.txt', shell=True)
                # with open('./pred.txt', encoding='utf-8') as f:
                #     msg = f.readline().strip()
                #     print(msg)
                #     await client.send_message(message.channel, msg)
                # await client.send_message(message.channel, str(message.content).replace(alpha[rnd], '🅱').replace(alpha[rnd].upper(), '🅱'))
            elif n1 == n2:
                await client.send_message(message.channel, 'https://media1.tenor.com/images/a0eb3bd86d78684a8e92858f428af621/tenor.gif?itemid=5913912')
    await client.process_commands(message)
    
#greet and give advice
@client.command()
async def greet(*args):
    await client.say(greet_txt)
    
#egg boy emoji
@client.command()
async def boost(*args):
    await client.say('You are most :egg:-cellent!')
 
#tulku'd
@client.command()
async def tulku(*args):
    tulku_list = tulku_memes
    await client.say('Blaze it my egg!')
    await client.say(str(random.sample(tulku_list, 1))[2:-2])
    
#second easter egg, the long easter egg
@client.command()
async def long_egg(*args):
    await client.say('Praise it!')
    await client.say('http://i0.kym-cdn.com/entries/icons/original/000/023/206/Screen_Shot_2017-06-13_at_3.54.19_PM.png')

#third easter egg, come to the sabbat    
@client.command()
async def sabbat(*args):
    await client.say(bw_text)
    await client.say('https://www.youtube.com/watch?v=TkC08sicP6Q')

#gives fortunes based on egg puns 40% of the time
@client.command()
async def fortune(*args):
    r = random.random()
    fortunes = fortune_list
    if r < 0.40:
        await client.say("Unable to crack the shell of the void :(")
    else:
        await client.say(str(random.sample(fortunes, 1))[2:-2])

#a third easter egg, shows a sugg-egg-stive photo
@client.command()
async def male_seggshual_organ(*args):
    await client.say('https://i.imgur.com/Cb6sgyi.jpg')

@client.command()
async def copypasta(*args):
    if r:
        random_post_number = random.randint(0,len(posts))
        await client.say(
            r.submission(posts[random_post_number]).selftext
        )


def transform_msg(msg):
    return re.sub(r'[eE]gg', '🥚', msg)





#clay
client.run('NDE3NDAxNDI1OTIwNzg2NDMz.DXSe4w.Cjy0mMdkwGLD3VslphhSx0bhgyM')
#mich
#client.run('NDIwMTg5MDI5MDA3NDkxMDgy.DYRGCg.OGca7tt-X7dxrSb0CfkqfcmPPb0')

