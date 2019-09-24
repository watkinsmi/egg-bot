import discord
import asyncio
from discord.ext.commands import Bot
import platform
import random
from egg_assets import greet_txt, tulku_memes, bw_text, fortune_list
import re

commands = dict()
vars = dict()
queue = []

'''
script = 'eggscript\n' \
         '0 for 0:3\n' \
       '1 print hello\n' \
       '2 end\n' \
       '3 number i 0\n' \
       '4 number j 2 \n' \
       '5 print true\n' \
       '6 ++ i\n' \
       '7 if < $i $j\n' \
       '8 print $i\n' \
       '9 goto 4\n' \
       '10 end\n' \
       '11 print $i\n' \
       '12 -- i\n' \
       '13 print $i'
'''
def for_loop(start, end):
    param = commands[start][4:]
    x = int(param[0:param.find(':')])
    y = int(param[param.find(':') + 1:])

    for i in range(x, y):
        for j, cmd in enumerate(range(start + 1, end)):
            queue.insert(j, cmd)

async def prnt(start, client, channel):
    param = commands[start][6:]
    if param.startswith('$'):
        print(vars.keys())
        var_name = param[1:]
        await client.send_message(channel, str(vars[var_name]))
    else:
        await client.send_message(channel, commands[start][6:])

def number(start):
    param = commands[start][7:]
    var_name = param[0:param.find(' ')]
    var_val = int(param[param.find(' ') + 1:])

    vars[var_name] = var_val

def incr(start):
    param = commands[start][3:]
    new_value = vars[param] + 1
    vars[param] = new_value

def decr(start):
    param = commands[start][3:]
    new_value = vars[param] - 1
    vars[param] = new_value

def boolean_operation(boolean_op, x, y):
    if boolean_op == '>':
        return x > y
    elif boolean_op == '<':
        return x < y
    elif boolean_op == '=':
        return x == y

#TODO: work on this
def if_statement(start, end):
    param = commands[start][3:]
    boolean_op = param[0:1]
    values = param[2:].split(' ')
    x = int(vars[values[0][1:]] if values[0].startswith('$') else values[0])
    y = int(vars[values[1][1:]] if values[1].startswith('$') else values[1])
    if boolean_operation(boolean_op, x, y):
        for j, cmd in enumerate(range(start + 1, end)):
            queue.insert(j, cmd)
    else:
        for j, cmd in enumerate(range(start, end)):
            queue.pop(0)


def goto(start):
    param = int(commands[start][5:])
    for j, cmd in enumerate(range(param, start + 1)):
        queue.insert(j, cmd)

async def parse(client, channel):
    while (len(queue) > 0):
        i = queue.pop(0)
        cmd = commands[i]
        print('current line: ' + str(i))
        print('current cmd: ' + cmd)
        print('current queue: ' + str(queue))

        if cmd.startswith('STOP'):
            while (len(queue) > 0):
                queue.pop()
        elif cmd.startswith('for'):
            end_for = -1
            for j in range(i, len(commands.keys())):
                if commands[j].startswith('end'):
                    end_for = j
                    break
            for_loop(i, end_for)
        elif cmd.startswith('print'):
            await prnt(i, client, channel)
        elif cmd.startswith('number'):
            number(i)
        elif cmd.startswith('++'):
            incr(i)
        elif cmd.startswith('--'):
            decr(i)
        elif cmd.startswith('if'):
            end_if = -1
            for j in range(i, len(commands.keys())):
                if commands[j].startswith('end'):
                    end_if = j
                    break
            if_statement(i, end_if)
        elif cmd.startswith('goto'):
            goto(i)

async def go(script, client, channel):
    for line in script.split(';'):
        if line.startswith('eggscript;') or len(line) == 0:
            continue
        lineInd = int(line[0:line.find(' ')])
        lineCommand = line[line.find(' ') + 1:]

        commands[lineInd] = lineCommand

        queue.append(lineInd)

    await parse(client, channel)

