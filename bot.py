# bot.py
import os # for importing env vars for the bot to use
from twitchio.ext import commands
import requests
import json

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

@bot.event
async def event_ready():

    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me est apparu dans le chat !")


@bot.event
async def event_message(ctx):

    # Le bot ignorera ses propres messages
    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
        return
    # Recherche d'une commande connu à executer.
    await bot.handle_commands(ctx)

    # Condition de réponse du bot Hors commande 
    if 'hello' in ctx.content.lower():
        await ctx.channel.send(f"Salut, @{ctx.author.name} !")


def flags(source, target):
    flag = ""
    if source == "FR":
        flag += "🇨🇵 ➔ " 
    elif source == "EN":
        flag += "🇬🇧 ➔ "
    elif source == "ES":
        flag += "🇪🇦 ➔ "
    elif source == "DE":
        flag += "🇩🇪 ➔ "
    else:
        flag += "❓ ➔ "
    
    if target == "FR":
        flag += "🇨🇵" 
    elif target == "EN":
        flag += "🇬🇧"
    elif target == "ES":
        flag += "🇪🇦"
    elif target == "DE":
        flag += "🇩🇪"
    else:
        flag += "❓"
    
    return flag

@bot.command(name='translate')
async def translate(ctx):
    await ctx.send(f"/me @{ctx.author.name} You can use translation bot by typing ?fr ?en ?es ?de followed by your message to translate it in the chat.")

@bot.command(name='fr')
async def fr(ctx):
    if len(ctx.content[3:]) <= 2:
        await ctx.send(f"/me @{ctx.author.name} , pour utiliser la commande de traduction veuillez faire ?fr [votre message] dans le chat. :)")
        return
    response = requests.get("https://api-free.deepl.com/v2/translate?auth_key=" + os.environ['DEEPL_TOKEN'] + "&text=" + ctx.content[3:] + "&target_lang=FR")
    print(response.json())
    traduction = json.loads(json.dumps(response.json()))
    # Choix des drapeaux
    answer = flags(traduction["translations"][0]["detected_source_language"], "FR")
    # End Choix des drapeaux
    await ctx.send(answer + ' : ' + traduction["translations"][0]["text"])

@bot.command(name='en')
async def en(ctx):
    if len(ctx.content[3:]) <= 2:
        await ctx.send(f"/me @{ctx.author.name} , to use translation command please enter ?en [your message] in the chat. :)")
        return
    response = requests.get("https://api-free.deepl.com/v2/translate?auth_key=" + os.environ['DEEPL_TOKEN'] + "&text=" + ctx.content[3:] + "&target_lang=EN")
    print(response.json())
    traduction = json.loads(json.dumps(response.json()))
    # Choix des drapeaux
    answer = flags(traduction["translations"][0]["detected_source_language"], "EN")
    # End Choix des drapeaux
    await ctx.send(answer + ' : ' + traduction["translations"][0]["text"])

@bot.command(name='de')
async def de(ctx):
    if len(ctx.content[3:]) <= 2:
        await ctx.send(f"/me @{ctx.author.name} , to use translation command please enter ?de [your message] in the chat. :)")
        return
    response = requests.get("https://api-free.deepl.com/v2/translate?auth_key=" + os.environ['DEEPL_TOKEN'] + "&text=" + ctx.content[3:] + "&target_lang=DE")
    print(response.json())
    traduction = json.loads(json.dumps(response.json()))
    # Choix des drapeaux
    answer = flags(traduction["translations"][0]["detected_source_language"], "DE")
    # End Choix des drapeaux
    await ctx.send(answer + ' : ' + traduction["translations"][0]["text"])

@bot.command(name='es')
async def es(ctx):
    if len(ctx.content[3:]) <= 2:
        await ctx.send(f"/me @{ctx.author.name} , to use translation command please enter ?de [your message] in the chat. :)")
        return
    response = requests.get("https://api-free.deepl.com/v2/translate?auth_key=" + os.environ['DEEPL_TOKEN'] + "&text=" + ctx.content[3:] + "&target_lang=ES")
    print(response.json())
    traduction = json.loads(json.dumps(response.json()))
    # Choix des drapeaux
    answer = flags(traduction["translations"][0]["detected_source_language"], "ES")
    # End Choix des drapeaux
    await ctx.send(answer + ' : ' + traduction["translations"][0]["text"])


if __name__ == "__main__":
    bot.run()