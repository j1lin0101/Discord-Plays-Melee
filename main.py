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

    if message.content.startswith("$help"):
        await message.channel.send("Smash on it's own is a rather complex game so trying to simplify it into pure text inputs is super difficult but I tried my best :)\n "
                                   "All commands will start with a ```$``` to let Discord know that you're inputting a command.")
        await message.channel.send("**Basic Movement**:\n"
                                   "```$left``` will make your character run left\n"
                                   "```$right``` will make your character run right\n"
                                   "```$crouch``` will make your character hold down (also useful for dropping through platforms)\n"
                                   "```$jump``` will make your character jump (note that your double jump will not come if you input a single message saying ```$jump $jump```. Inputs are one per messsage)")
        await message.channel.send("**Attacks**\n"
                                   "All attacks are done by writing the direction letter (i.e. l for left, r for right, u for up, d for down) in combination with the action\n"
                                   "```$jab``` since jab does not take a direction just typing the command as is will make your character jab\n"
                                   "*Smash Attacks*\n"
                                   "Smash Attacks are hard hitting kill moves. Type the directional letter and smash to perform the action\n"
                                   "```$lsmash``` will perform a side smash to the left\n"
                                   "```$rsmash``` will perform a side smash to the right\n"
                                   "```$usmash``` will perform an upward smash attack\n"
                                   "```$dsmash``` will perform a downward smash attack\n"
                                   "*Tilts*\n"
                                   "Tilts are physical attacks like smash attacks. However they sometimes lack the instant kill power in exchange for speed and combo potential\n"
                                   "```$ltilt``` will perform a side tilt to the left\n"
                                   "```$rtilt``` will perform a side tilt to the right\n"
                                   "```$utilt``` will perform an upward tilt attack\n"
                                   "```$dtilt``` will perform a downward tilt attack")
        await message.channel.send("**Special Attacks**\n"
                                   "Your specials are what make your character unique. They can be projectiles, strong hits, or super situational moves like a reflector (unless you actually know how to play spacies in this game)\n"
                                   "Simply typing the directional letter and b will perform that special\n"
                                   "```$lb``` will perform a side special to the left\n"
                                   "```$rb``` will perform a side special to the right\n"
                                   "```$ub``` will perform an up special. Note that Up Special is normally your recovery move. Pay special attention when to type this in as quickly as you can when you're offstage\n"
                                   "```$dtilt``` will perform a downward special")
        await message.channel.send("If you have any more questions feel free to ask @boi_jiro\n")

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

    print("Player 1: ", end=" ")

    # MOVEMENT
    if message.content.startswith('$left'):
        print("going left")
        pressKey('q')

    if message.content.startswith('$right'):
        print("going right")
        pressKey('d')

    if message.content.startswith('$jump'):
        print("jumping")
        pressKey('w')

    if message.content.startswith('$crouch'):
        print("crouching")
        pressKey('s')

    # TRIGGERS
    if message.content.startswith('$shield'):
        print("shielding")
        pressKey('z')

    if message.content.startswith('$grab'):
        print("grabbing")
        pressKey('e')

    # SMASH ATTACKS
    if message.content.startswith('$rsmash'):
        print("right smash")
        pressKey('v')

    if message.content.startswith('$lsmash'):
        print("left smash")
        pressKey('c')

    if message.content.startswith('$usmash'):
        print("up smash")
        pressKey('r')

    if message.content.startswith('$dsmash'):
        print("down smash")
        pressKey('f')

    # TILTS AND JAB
    if message.content.startswith('$jab'):
        print("jabbing")
        pressKey('b')

    if message.content.startswith('$ltilt'):
        print("left tilt")
        keyComboMod('g', 'q', 'b')

    if message.content.startswith('$rtilt'):
        print("right tilt")
        keyComboMod('g', 'd', 'b')

    if message.content.startswith('$utilt'):
        print("up tilt")
        keyComboMod('g', 'w', 'b')

    if message.content.startswith('$dtilt'):
        print("down tilt")
        keyComboMod('g', 's', 'b')

    # SPECIALS
    if message.content.startswith('$b'):
        print("netural b")
        pressKey('x')

    if message.content.startswith('$lb'):
        print("left b")
        keyCombo('x', 'q')

    if message.content.startswith('$rb'):
        print("right b")
        keyCombo('x', 'd')

    if message.content.startswith('$db'):
        print("down b")
        keyCombo('x', 's')

    if message.content.startswith('$ub'):
        print("up b")
        keyCombo('x', 'w')

def player2Act(message):

    print("Player 2: ", end=" ")

    # MOVEMENT
    if message.content.startswith('$left'):
        print("going left")
        pressKey('j')

    if message.content.startswith('$right'):
        print("going right")
        pressKey('l')

    if message.content.startswith('$jump'):
        print("jumping")
        pressKey('i')

    if message.content.startswith('$crouch'):
        print("crouching")
        pressKey('k')

    # TRIGGERS
    if message.content.startswith('$shield'):
        print("shielding")
        pressKey('o')

    if message.content.startswith('$grab'):
        print("grabbing")
        pressKey('y')

    # SMASH ATTACKS
    if message.content.startswith('$rsmash'):
        print("right smash")
        pressKey('-')

    if message.content.startswith('$lsmash'):
        print("left smash")
        pressKey('[')

    if message.content.startswith('$usmash'):
        print("up smash")
        pressKey('u')

    if message.content.startswith('$dsmash'):
        print("down smash")
        pressKey(']')

    # TILTS AND JAB
    if message.content.startswith('$jab'):
        print("jabbing")
        pressKey('n')

    if message.content.startswith('$ltilt'):
        print("left tilt")
        keyComboMod('h', 'j', 'n')

    if message.content.startswith('$rtilt'):
        print("right tilt")
        keyComboMod('h', 'l', 'n')

    if message.content.startswith('$utilt'):
        print("up tilt")
        keyComboMod('h', 'i', 'n')

    if message.content.startswith('$dtilt'):
        print("down tilt")
        keyComboMod('h', 'k', 'n')

    # SPECIALS
    if message.content.startswith('$b'):
        print("netural b")
        pressKey('m')

    if message.content.startswith('$lb'):
        print("left b")
        keyCombo('m', 'j')

    if message.content.startswith('$rb'):
        print("right b")
        keyCombo('m', 'l')

    if message.content.startswith('$db'):
        print("down b")
        keyCombo('m', 'k')

    if message.content.startswith('$ub'):
        print("up b")
        keyCombo('m', 'i')

client.run(TOKEN)