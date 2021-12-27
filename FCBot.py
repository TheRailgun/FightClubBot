import discord 

client = discord.Client()

modifier = '$'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(modifier+'hello'):
        await message.channel.send('Hello!')

client.run('OTI0Nzc4MTk0NDE3MTIzMzQ4.Ycjgzw.WKcYPPOjipxRptsl7q9a4-tKVJg')