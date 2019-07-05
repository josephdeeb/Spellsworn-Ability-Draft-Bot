import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

def interpretNames(message):
    # To get to this point, message must begin with "s! draft ", and it must've come from a text channel
    # Now we want it to include names of discord users in the server from which the message came
    users = message.content[9:].split(" @")
    channelMembers = message.channel.members()
    if len(users) >= 1:
        for i in range(len(users)):
            if channelMembers[i].

@client.event
async def on_message(message):
    if message.content[:3] == "s! ":
        if message.content[3:9].lower() == "draft ":
            #Haven't tested if this is always true even if its a DMChannel
            if type(message.channel) == discord.TextChannel:
                users = interpretNames(message)
                if users == False:
                    # names supplied <= 1
