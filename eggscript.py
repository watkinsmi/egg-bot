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
       '4 print true\n' \
       '5 ++ i\n' \
       '6 if < $i 2\n' \
       '7 print $i\n' \
       '8 goto 4\n' \
       '9 end\n' \
       '10 print $i\n' \
       '11 -- i\n' \
       '12 print $i'
'''

def for_loop(start, end):
    param = commands[start][4:]
    x = int(param[0:param.find(':')])
    y = int(param[param.find(':') + 1:])

    for i in range(x, y):
        for j, cmd in enumerate(range(start + 1, end)):
            queue.insert(j, cmd)

def prnt(start):
    param = commands[start][6:]
    if param.startswith('$'):
        var_name = param[1:]
        print(str(vars[var_name]))
    else:
        print(commands[start][6:])

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
    for j, cmd in enumerate(range(param, start)):
        queue.insert(j, cmd)

def parse():
    while (len(queue) > 0):
        i = queue.pop(0)
        cmd = commands[i]
        if cmd.startswith('for'):
            end_for = -1
            for j in range(i, len(commands.keys())):
                if commands[j].startswith('end'):
                    end_for = j
                    break
            for_loop(i, end_for)
        elif cmd.startswith('print'):
            prnt(i)
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

def go(script):
    for line in script.splitlines():
        lineInd = int(line[0:line.find(' ')])
        lineCommand = line[line.find(' ') + 1:]

        commands[lineInd] = lineCommand

        queue.append(lineInd)

    parse()
'''
go(script)

code = ''
for line in script.splitlines():
    if line.startswith('eggscript'):
        continue
    code += line + '\n'
go(code)
'''
