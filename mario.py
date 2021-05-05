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
TOKEN = os.getenv('MARIO_TOKEN')

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



@client.event
async def on_ready():
    print('{client.user} has connected to Discord!')
    if active_game:
        print("Game Activated")
    else:
        print("Game Deactivated")

active_game = False

@client.event
async def on_message(message):

    global active_game
    
    if active_game:
        playerAct(message)

    if message.content.startswith("$help"):
        await message.channel.send("**Basic Movement**:\n"
                                   "```$left```will make Mario move left\n"
                                   "```$right```will make Mario move right\n"
                                   "```$jump```will make Mario jump")
        await message.channel.send("**Other Stuff**:\n"
                                   "```$runr```will make Mario run right\n"
                                   "```$runl```will make Mario move left\n"
                                   "```$jumpr```will make Mario jump to the right\n"
                                   "```$jumpl```will make Mario jump to the left")


    if message.content.startswith("$start"):
        active_game = True
        print("Starting Game")
        bot_msg = await message.channel.send("LESSAGO")


    if message.content.startswith("$end"):
        active_game = False
        print("Ending Game")




def playerAct(message):

    # Configure GC Controller Buttons to Keyboard Keys
    up = 'w'
    down = 's'
    left = 'a'
    right = 'd'
    start = Key.shift_l
    select = Key.cmd_l
    a = 'x'
    b= 'z'

    print("Player: ", end=" ")

    # MOVEMENT
    if message.content.startswith('$left'):
        print("going left")
        pressKey(left)

    if message.content.startswith('$right'):
        print("going right")
        pressKey(right)

    if message.content.startswith('$jump'):
        print("jumping")
        pressKey(a)

    if message.content.startswith('$crouch'):
        print("crouching")
        pressKey(down)

    #COMBINED MOVEMENT

    if message.content.startswith('$jumpr'):
        print("jumping right")
        keyCombo(up, right)

    if message.content.startswith('$jumpl'):
        print("jumping left")
        keyCombo(up, left)

    if message.content.startswith('$runr'):
        print("running right")
        keyCombo(b, right)
    
    if message.content.startswith('$runl'):
        print("running left")
        keyCombo(b, left)

client.run(TOKEN)