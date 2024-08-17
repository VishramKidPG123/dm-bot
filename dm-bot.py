import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

players = {}

registered_messages = []

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel('CHANNEL_ID') 
    register_message = await channel.send("Please react to this message to be registed as a player!")
    await register_message.add_reaction('✅')
    registered_messages.append(register_message)

@client.event
async def on_message(message):
    if message.content.startswith('!list'):
        dm_role = discord.utils.get(message.author.roles, name="DM")
        if dm_role is None:
            return
        grouped_data = {}
        for key, value in players.items():
            if value not in grouped_data:
                grouped_data[value] = []
            grouped_data[value].append(key)
        #await message.channel.send(str(players))

        embed = discord.Embed(
            title="Grouped Data",
            description="Here are the keys grouped by their values:",
            color=discord.Color.blue()
        )

        embed=discord.Embed(title="List")
        for value, keys in grouped_data.items():
        # Join the keys into a single string, separated by commas
            keys_str = "\n".join(keys)
        # Add a field to the embed
            embed.add_field(name=value, value=keys_str, inline=False)
        await message.channel.send(embed=embed)
    
    if message.content.startswith('!move'):
        dm_role = discord.utils.get(message.author.roles, name="DM")
        if dm_role is None:
            return
        msg = message.content.split()
        if len(msg) < 3 or len(msg) > 3:
           await message.channel.send("Incorrect usage! Should be: !move [player] [sector]")
           return 
        elif len(msg) == 3: #msg[1] = user, msg[2] = sector
            if msg[1] in players:
                players[msg[1]] = msg[2]
            else:
                await message.channel.send("No such registered player found!")
                print(msg[1])
                return


@client.event
async def on_reaction_add(reaction, user):
    if reaction.message == registered_messages[0]:
        players[user.name] = 'Default-Sector'

client.run('TOKEN')
