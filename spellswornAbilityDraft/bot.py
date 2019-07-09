import discord
import spellData
from enum import Enum

client = discord.Client()

class SpellPack:
    def __init__(self, spells=[]):
        self.spells = spells

class DraftMember:
    def __init__(self, player):
        # discord.member this DraftMember represents
        self.player = player
        # Spells this DraftMember has drafted
        self.pool = []
        # Pack this DraftMember is currently drafting
        self.pack = -1


"""
Two major ways to do the drafts:
    1) The amount of a single spell you draft is the amount you're allowed to level it up
        i.e. If you draft two magic missile spells, you can level magic missile up to level 2 but not level 3
    2) When you draft a spell, you can level it as many times as you want
        A) No multiples of spells at all
        B) No multiples of spells in singular packs, but separate packs can contain the same spell
        C) Packs can contain multiples of any spells

    For the time being I'm going to assume 2) B)
"""
class DraftGroup:
    defaultSpellSlots = []

    def __init__(self, id, players):
        # Identifier of the draft group
        self.id = id
        # All discord.members in the draft group
        self.players = players
        # All the packs being passed around
        self.packs = []

    # Initialize all the packs for each player
    def initializePacks(self, spellSlots):

        # For each player
        for i in range(len(self.players)):



# Dictionary that contains all users who have either sent or been mentioned in a draft command.
# userID:(playingStatus(bool), DraftGroupID)
userStatuses = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content[:3] == "s! ":
        if message.content[3:9].lower() == "draft ":
            #Haven't tested if this is always true even if its a DMChannel
            if type(message.channel) == discord.TextChannel:
                users = message.mentions + [message.author]
