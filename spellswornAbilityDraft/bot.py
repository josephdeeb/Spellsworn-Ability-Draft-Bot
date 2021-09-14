import discord
import spellData
import random
import asyncio
from enum import Enum

client = discord.Client()

drafts = 0

class SpellPack:
    def __init__(self, spells=[]):
        self.spells = spells

class DraftMember:
    def __init__(self, player):
        # discord.member this DraftMember represents
        self.player = player
        # Spells this DraftMember has drafted
        self.pool = []
        # Index of the pack this DraftMember is currently drafting
        self.pack = -1
        # Whether or not the DraftMember has picked a card from their pack
        self.picked = False
        # Card that the player has picked
        self.pick = -1

    async def displayPack(self, pack):
        spellCount = 1
        message = ''
        for spell in pack:
            message += '\n__**{}**__  Spell name: **{}**'.format(spellCount, spell.name)
            message += '\n{}      Type:   **{}**\n'.format(' '*len(str(spellCount)), spell.type.name)
            spellCount += 1
        return message

    async def getID(self):
        return self.player.id


"""
Two major ways to do the drafts:
    1) The amount of a single spell you draft is the amount you're allowed to level it up
        i.e. If you draft two magic missile spells, you can level magic missile up to level 2 but not level 3
    2) When you draft a spell, you can level it as many times as you want
        A) No multiples of spells at all
        B) No multiples of spells in singular packs, but separate packs can contain the same spell
        C) Packs can contain multiples of any spells

    For the time being I'm going to assume 2) B)

PACK COMPOSITION
    2) B) composition
        1x Offensive 1x Travel rest are Random Spells (no repeats in pack)
"""
class DraftGroup:
    defaultSpellSlots = []

    def __init__(self, id, channel, players=[], packSize=8):
        # Identifier of the draft group
        self.id = id
        # List of all DraftMembers in the draft group
        self.players = players
        # Size of packs
        if packSize <= 1:
            raise ValueError
        self.packSize = packSize
        # All the packs being passed around
        self.packs = []
        # The channel from which the start draft command was issued
        self.initialChannel = channel

    # Takes a list of members / users and converts them into DraftMembers then adds them to self.players
    async def addPlayers(self, users):
        for user in users:
            self.players += [DraftMember(user)]

    # Initialize all the packs for each player
    async def initializePacks(self):
        # For each player
        for i in range(0, len(self.players)):
            chosenSpells = dict()
            pack = [-1 for x in range(self.packSize)]
            # Set first two packs to one offensive spell and one travel spell
            pack[0] = random.choice(spellData.offensiveSpells)
            chosenSpells[pack[0]] = 1
            pack[1] = random.choice(spellData.travelSpells)
            chosenSpells[pack[1]] = 1
            # For each remaining slot in the pack
            for j in range(2, self.packSize):
                """
                BUG NOTE: This will overflow if all spells are already chosen, should only
                happen if packSize exceeds total amount of spells
                """
                # Fill the slot with a random spell, no repeats
                pack[j] = random.choice(spellData.allSpells)
                while pack[j] in chosenSpells:
                    pack[j] = random.choice(spellData.allSpells)
                chosenSpells[pack[j]] = 1
            # Finally, add the pack to self.packs and set the appropriate player's pack index to i
            self.packs += [pack]
            self.players[i].pack = i

    # Sends a private message to each player of their pack, and asks for a response
    async def displayPacks(self):
        # For each player in this draft group
        for member in self.players:
            # Send that player a message that displays the pack they currently have
            await member.player.send(await member.displayPack(self.packs[member.pack]))

    # Checks if all players have picked their card and are ready to pass their packs
    async def checkReady(self):
        for member in self.players:
            if member.picked == False:
                return False

        return True

    # Retrieves a DraftMember given their id
    async def getDraftMember(self, id):
        for player in self.players:
            playerID = await player.getID()
            if playerID == id:
                return player

        return False

    # Passes packs from player to player then sends out a new pack message
    async def passPacks(self):
        for player in self.players:
            # Take the card that player has picked and add it to their pool
            pack = self.packs[player.pack]
            player.pool += [pack[player.pick]]
            # Remove the card from the pack
            del pack[player.pick]
            # Now select the next pack and reset any relevant variables
            if player.pack >= (len(self.players)-1):
                player.pack = 0

            else:
                player.pack += 1

            player.picked = False
            player.pick = -1

# Dictionary that contains all users who have either sent or been mentioned in a draft command.
# userID:(playingStatus(bool), DraftGroupID)
userStatuses = {}

# Dictionary that contains all currently running draft groups
# DraftGroup.id: DraftGroup
draftGroups = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    drafts = 0

@client.event
async def on_message(message):
    if message.content == 's! quit':
        exit()
    if message.author == client.user:
        return
    if type(message.channel) == discord.TextChannel:
        if message.content[:3] == 's! ':
            if message.content[3:9].lower() == 'draft ':
                    users = message.mentions + [message.author]
                    # Create the string of mentions for the initialization message
                    mentions = ''
                    for user in users:
                        mentions += user.mention + ', '
                    # Send the initialization message
                    await message.channel.send('Starting draft with: {}'.format(mentions))

                    # Create the actual DraftGroup
                    global drafts
                    group = DraftGroup(drafts, message.channel)
                    await group.addPlayers(users)
                    global draftGroups
                    draftGroups[group.id] = group
                    global userStatuses
                    # Set the drafting status of all players
                    for user in users:
                        userStatuses[user.id] = (True, drafts)
                    # Increment amount of drafts
                    drafts += 1

                    # Initialize the packs
                    await group.initializePacks()

                    # Finally, display the packs to the players
                    await group.displayPacks()

    # Handling a DM, should be a message that tells the bot what pick to take from a pack
    elif type(message.channel) == discord.DMChannel:
        if message.author.id in userStatuses:
            # If that user is in a draft and the draft id is not -1
            if userStatuses[message.author.id][0] == True and userStatuses[message.author.id][1] != -1:
                # Ensure the input is an integer
                if message.content.isdigit():
                    selection = int(message.content)
                    # Retrieve the draftGroup
                    group = draftGroups[userStatuses[message.author.id][1]]
                    # Retrieve the DraftMember
                    member = await group.getDraftMember(message.author.id)
                    # Ensure the input is within the range of acceptable values given the size of the pack
                    if selection < 1 or selection > len(group.packs[member.pack]):
                        await message.channel.send('That selection does not exist, please try again.')
                    # That selection does exist, so time to set that to the player's pick and set the picked flag
                    else:
                        member.pick = selection - 1
                        member.picked = True
                        await message.channel.send('Your selection is: {}'.format(group.packs[member.pack][selection-1].name))
                        # Now check to see if all players have picked their cards.  If so, we're ready to pass the packs
                        if await group.checkReady():
                            # If there's only one card left in our pack then this pack is done
                            if len(group.packs[member.pack]) == 1:
                                await group.passPacks()
                                finalMessage = ''
                                for drafter in group.players:
                                    finalMessage += '\n{}\'s spells: '.format(drafter.player.mention)
                                    for spell in drafter.pool:
                                        finalMessage += '{}, '.format(spell.name)

                                    finalMessage += '\n'

                                await group.initialChannel.send(finalMessage)

                            else:
                                await group.passPacks()
                                await group.displayPacks()

            else:
                await message.channel.send('You are not currently in a draft.')
        # message author isn't in a draft, let them know
        else:
            await message.channel.send('You are not currently in a draft.')

#client.run(INSERT TOKEN STRING HERE)
