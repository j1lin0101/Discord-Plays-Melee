import os
import time
import subprocess
import ctypes
import random
import string

import discord
from discord.ext import commands


from dotenv import load_dotenv

from pynput.keyboard import Key, Controller

keyboard = Controller()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='.', case_insensitive=True)

# KEYBOARD ACTIONS
# SIMPLE KEY PRESS + RELEASE (E.G. MOVEMENT, SMASH ATTACKS, SHIELDING)
def pressKey(key):
    keyboard.press(key)
    time.sleep(.1)
    keyboard.release(key)

# BUTTON COMBINATIONS (E.G. DIRECTION + SPECIAL)
def keyCombo(action, direction):
    keyboard.press(action)
    keyboard.press(direction)
    time.sleep(.02)
    keyboard.release(action)
    keyboard.release(direction)

# BUTTON COMBOS THAT USE MODIFIERS (E.G. TILTS)
def keyComboMod(modifier, direction, action):
    keyboard.press(modifier)
    keyboard.press(direction)
    time.sleep(.04)
    keyboard.press(action)
    time.sleep(.02)
    keyboard.release(modifier)
    keyboard.release(direction)
    keyboard.release(action)

# BUTTON COMBO THAT INCORPORATES AERIALS
def keyComboAerial(jump, action):
    pressKey(jump)
    pressKey(action)




@client.event
async def on_ready():
    print('{client.user} has connected to Discord!')
    if active_game:
        print("Game Activated")
    else:
        print("Game Deactivated")

active_game = False
player1 = []
player2 = []

@client.event
async def on_message(message):

    global active_game
    global player1
    global player2

    if active_game:
        #Player 1
        if message.author.name in player1:
            player1Act(message)

        #Player 2
        if message.author.name in player2:
            player2Act(message)

        time.sleep(.16)

    if message.content.startswith("$help"):
        await message.channel.send("Smash on it's own is a rather complex game so trying to simplify it into pure text inputs is super difficult but I tried my best :)\n "
                                   "All commands will start with a ```$``` to let Discord know that you're inputting a command.")
        await message.channel.send("**Basic Movement**:\n"
                                   "```$left```will make your character run left\n"
                                   "```$right```will make your character run right\n"
                                   "```$crouch```will make your character hold down (also useful for dropping through platforms)\n"
                                   "```$jump```will make your character jump (note that your double jump will not come if you input a single message saying ```$jump $jump```. Inputs are one per messsage)")
        await message.channel.send("**Attacks**\n"
                                   "```$jab``` will make your character jab \n"
                                   "```$b``` will make your character do their neutral (no direction) special move\n"
                                   "```$nair``` will make your character do a neutral (no directional focus) aerial attack\n"
                                   "***Directional Attacks***\n"
                                   "All attacks (smash attacks, tilts, aerials, and specials) are done by writing the direction letter (i.e. l for left, r for right, u for up, d for down) in combination with the action (smash, tilt, b,)\n"
                                   "***Examples***\n"
                                   "```$lsmash```A Smash Attack to the left\n"
                                   "```$dtilt```A Downward Tilt Attack\n"
                                   "```$rair``` An Aerial toward the Right side\n"
                                   "```$ub```An Upward Special")
        await message.channel.send("If you have anymore questions please feel free to DM @boi_jiro with questions")


    if message.content.startswith("$start"):
        active_game = True
        print("Starting Game")
        bot_msg = await message.channel.send("Select Your Team")
        one_react = await bot_msg.add_reaction("1️⃣")
        two_react = await bot_msg.add_reaction("2️⃣")

    if message.content.startswith("$end"):
        active_game = False
        print("Ending Game")
        player1 = []
        player2 = []


@client.event
async def on_reaction_add(reaction, user):
    global player1
    global player2


    if reaction.emoji == "1️⃣":

        if user.name in player2 and user.name != 'discord-plays':
            player2.remove(user.name)
            await reaction.message.remove_reaction("2️⃣", user)

        print(user.name + " added to Player 1")
        player1.append(user.name)
        print(player1)

    if reaction.emoji == "2️⃣":

        if user.name in player1 and user.name != 'discord-plays':
            player1.remove(user.name)
            await reaction.message.remove_reaction("1️⃣", user)

        print(user.name + " added to Player 2")
        player2.append(user.name)
        print(player2)


def player1Act(message):

    # Configure GC Controller Buttons to Keyboard Keys
    up = 'e'
    down = 'd'
    left = 's'
    right = 'f'
    taunt = Key.tab
    c_up = Key.shift_l
    c_down = Key.cmd_l
    c_left = Key.ctrl_l
    c_right = Key.alt_l
    l = 'q'
    r = 'w'
    z = 'g'
    a = 'z'
    b = 'x'
    x = 'c'
    y = 'v'
    mod = 'r'
    start = Key.space

    print("Player 1: ", end=" ")

    # MOVEMENT
    if message.content.startswith('$left'):
        print("going left")
        pressKey(left)

    if message.content.startswith('$right'):
        print("going right")
        pressKey(right)

    if message.content.startswith('$jump'):
        print("jumping")
        pressKey(y)

    if message.content.startswith('$crouch'):
        print("crouching")
        pressKey(down)

    if message.content.startswith('$taunt'):
        print("taunting")
        pressKey(taunt)

    # TRIGGERS
    if message.content.startswith('$shield'):
        print("shielding")
        pressKey(l)

    if message.content.startswith('$grab'):
        print("grabbing")
        pressKey(z)

    # SMASH ATTACKS
    if message.content.startswith('$rsmash'):
        print("right smash")
        pressKey(c_right)

    if message.content.startswith('$lsmash'):
        print("left smash")
        pressKey(c_left)

    if message.content.startswith('$usmash'):
        print("up smash")
        pressKey(c_up)

    if message.content.startswith('$dsmash'):
        print("down smash")
        pressKey(c_down)

    # TILTS AND JAB
    if message.content.startswith('$jab'):
        print("jabbing")
        pressKey(a)

    #Mod, Direction, Action
    if message.content.startswith('$ltilt'):
        print("left tilt")
        keyComboMod(mod, left, a)

    if message.content.startswith('$rtilt'):
        print("right tilt")
        keyComboMod(mod, right, a)

    if message.content.startswith('$utilt'):
        print("up tilt")
        keyComboMod(mod, up, a)

    if message.content.startswith('$dtilt'):
        print("down tilt")
        keyComboMod(mod, down, a)

    # SPECIALS
    # Action, Direction
    if message.content.startswith('$b'):
        print("netural b")
        pressKey(b)

    if message.content.startswith('$lb'):
        print("left b")
        keyCombo(b, left)

    if message.content.startswith('$rb'):
        print("right b")
        keyCombo(b, right)

    if message.content.startswith('$db'):
        print("down b")
        keyCombo(b, down)

    if message.content.startswith('$ub'):
        print("up b")
        keyCombo(b, up)

    # AERIALS
    if message.content.startswith('$nair'):
        print("neutral air")
        keyComboAerial(y, a)

    if message.content.startswith('$rair'):
        print("right air")
        keyComboAerial(y, c_right)

    if message.content.startswith('$lair'):
        print("left air")
        keyComboAerial(y, c_left)

    if message.content.startswith('$dair'):
        print("down air")
        keyComboAerial(y, c_down)

def player2Act(message):
    # Configure GC Controller Buttons to Keyboard Keys
    up = 'u'
    down = 'j'
    left = 'h'
    right = 'k'
    taunt = Key.enter
    c_up = 'p'
    c_down = ';'
    c_left = 'l'
    c_right = "'"
    l = 'i'
    r = 'o'
    z = ','
    a = 'n'
    b = 'm'
    x = '['
    y = ']'
    mod = 'y'
    start = '.'

    print("Player 2: ", end=" ")

    # MOVEMENT
    if message.content.startswith('$left'):
        print("going left")
        pressKey(left)

    if message.content.startswith('$right'):
        print("going right")
        pressKey(right)

    if message.content.startswith('$jump'):
        print("jumping")
        pressKey(y)

    if message.content.startswith('$crouch'):
        print("crouching")
        pressKey(down)

    if message.content.startswith('$taunt'):
        print("taunting")
        pressKey(taunt)

    # TRIGGERS
    if message.content.startswith('$shield'):
        print("shielding")
        pressKey(l)

    if message.content.startswith('$grab'):
        print("grabbing")
        pressKey(z)

    # SMASH ATTACKS
    if message.content.startswith('$rsmash'):
        print("right smash")
        pressKey(c_right)

    if message.content.startswith('$lsmash'):
        print("left smash")
        pressKey(c_left)

    if message.content.startswith('$usmash'):
        print("up smash")
        pressKey(c_up)

    if message.content.startswith('$dsmash'):
        print("down smash")
        pressKey(c_down)

    # TILTS AND JAB
    if message.content.startswith('$jab'):
        print("jabbing")
        pressKey(a)

    # Mod, Direction, Action
    if message.content.startswith('$ltilt'):
        print("left tilt")
        keyComboMod(mod, left, a)

    if message.content.startswith('$rtilt'):
        print("right tilt")
        keyComboMod(mod, right, a)

    if message.content.startswith('$utilt'):
        print("up tilt")
        keyComboMod(mod, up, a)

    if message.content.startswith('$dtilt'):
        print("down tilt")
        keyComboMod(mod, down, a)

    # SPECIALS
    # Action, Direction
    if message.content.startswith('$b'):
        print("netural b")
        pressKey(b)

    if message.content.startswith('$lb'):
        print("left b")
        keyCombo(b, left)

    if message.content.startswith('$rb'):
        print("right b")
        keyCombo(b, right)

    if message.content.startswith('$db'):
        print("down b")
        keyCombo(b, down)

    if message.content.startswith('$ub'):
        print("up b")
        keyCombo(b, up)

    # AERIALS
    if message.content.startswith('$nair'):
        print("neutral air")
        keyComboAerial(y, a)

    if message.content.startswith('$rair'):
        print("right air")
        keyComboAerial(y, c_right)

    if message.content.startswith('$lair'):
        print("left air")
        keyComboAerial(y, c_left)

    if message.content.startswith('$dair'):
        print("down air")
        keyComboAerial(y, c_down)


client.run(TOKEN)