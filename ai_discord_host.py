import main
import ai_speaker
import discord

TOKEN = 'YOUR_DISCORD_TOKEN'
client = discord.Client()
responser = ai_speaker.Speaker('female')

@client.event
async def on_message(message):
    reply = ' '
    msg = ''
    msg_split = ''
    if message.author.bot:
        return

    msg = message.content
    print("msg:",msg)
    reply=main.Start_hosting(msg)
    await message.channel.send(reply)
    responser.Speak(str(msg))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
