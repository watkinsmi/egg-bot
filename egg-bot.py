# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import random

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Egg Bot", command_prefix="egg-", pm_help = False)

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
    elif str(message.author.name) != 'Egg Bot':
        n1, n2 = create_random_comparison()
        if n1 == n2:
            await client.send_message(message.channel, 'Eggcellent communication my dude!')
    await client.process_commands(message)
    
#greet and give advice
@client.command()
async def greet(*args):
    await client.say('''Welcome to Egg-Server young hatchling!
                     ------------------------------------------
                     I have a number of useless commands, and at least one easter egg...
                     -----------------------------------------------------------------
                     Use the prefix "egg-" to use the following commands
                     ---------
                     Commands: 
                     1) test - Tests the eggcasting service.
                     2) users - Gives user information about Egg-Server inhabitants.
                     3) fortune - Provides the user with a glimpse into their future.
                     4) boost - Ask Egg bot for a confidence boost!
                     ----------
                     More to come...maybe...
                     ''')
    
#egg boy emoji
@client.command()
async def boost(*args):
    await client.say('You are more :egg:-cellent!')
    
       
#gives fortunes based on egg puns 50% of the time
@client.command()
async def fortune(*args):
    r = random.random()
    fortune_list = ['Your future is most eggcellent!', 'You are eggsactly where you are supposed to be!',
                    'Eggciting things in your future!', 'For a long life, eat eggs and get some eggercise.',
                    'Eggstreme success in your future', 'Eggsplosive news coming your way', 'Eggstatic news coming!',
                    'You are walking on egg-shells my friend.', 'Eggstreme hardships coming friend.', 'Your future is simply eggstravagent.',
                    'Eggceptionally good luck coming your way.', 'Eggceptionally bad luck coming your way.', 'A rotten egg comes your way...',
                    'Your weekend will be scrambled.', 'Your future looks hard boiled friend.', 'Don\'t egg-nore the good news coming to you soon.',
                    'Simply....EGGCELLENT!', 'You will need to break a few eggs soon.']
    if r < 0.40:
        await client.say("Unable to crack the shell of the void :(")
    else:
        await client.say(str(random.sample(fortune_list, 1))[2:-2])
        

    
    	
client.run('NDE3NDAxNDI1OTIwNzg2NDMz.DXSe4w.Cjy0mMdkwGLD3VslphhSx0bhgyM')

