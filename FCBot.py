#Discord bot imports
import discord 
from discord.ext import commands
import os

#Google sheet imports. Might need to be installed locally. Used this guide https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/
import gspread
from oauth2client.service_account import ServiceAccountCredentials


#Google Sheets Script Below
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

bot_key = os.environ.get('DISCORD_TOKEN')

gdoc_json = os.environ.get('VHFC_JSON')

creds = ServiceAccountCredentials.from_json_keyfile_name('VHFC_JSON', scope)

client = gspread.authorize(creds)

sheet = client.open('VH Fight Club') #NAME OF SPREADSHEET OR URL

# Name of tab in spreedsheet
sheet_instance = sheet.worksheet('Fight Bookkeeping')

#Bot Script Below
bot = commands.Bot(command_prefix= '$')

@bot.event
async def on_ready():
    #await bot.change_presence(activity=discord.Game('Bets Closed!'))
    print('Bot is Running.')

@bot.command
async def displayembed():
    embed = discord.Embed(
        title = 'Betting Odds',
        description = 'These are the current odds for the match being bet on!',
        colour = discord.Colour.red()
    )

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency*1000)}')
    await ctx.send(gdoc_json)
    

#@bot.command()
#async def closed(ctx):
#    await bot.change_presence(activity=discord.Game('Bets Closed!'))


@bot.command(aliases=['odds','bet','underdog'])
@commands.has_role("Fight Club Staff")
async def bets(ctx):
    placeholderReturn = "190k"
    teams = 4
    underdogExists = False
    if((sheet_instance.acell('X7').value != "0") and (sheet_instance.acell('X7').value != "0k")):
        teams += 1
    if((sheet_instance.acell('X6').value != "0") and (sheet_instance.acell('X6').value != "0k")):
        teams += 1
        
    print(str(teams) + " teams fighting.")
    underdog = [''] * teams
    underdogBalance = [''] * teams
    team1 = 'team1Name'
    team2 = 'team2Name'
    team3 = 'team3Name'
    team4 = 'team4Name'

    team1 = sheet_instance.acell('B2').value
    if(sheet_instance.acell('X2').value == "#DIV/0!"):
        team1Odds = placeholderReturn
    else: 
        team1Odds = sheet_instance.acell('X2').value
    team2 = sheet_instance.acell('B3').value
    if(sheet_instance.acell('X3').value == "#DIV/0!"):
        team2Odds = placeholderReturn
    else:
        team2Odds = sheet_instance.acell('X3').value
    team3 = sheet_instance.acell('C2').value
    if(sheet_instance.acell('X4').value == "#DIV/0!"):
        team3Odds = placeholderReturn
    else:
        team3Odds = sheet_instance.acell('X4').value
    team4 = sheet_instance.acell('C3').value
    if(sheet_instance.acell('X5').value == "#DIV/0!"):
        team4Odds = placeholderReturn
    else:
        team4Odds = sheet_instance.acell('X5').value

    matchText = team1 + " vs " + team2 + " vs " + team3 + " vs " + team4
    if(teams > 4):
        team5 = sheet_instance.acell('B4').value
        if(sheet_instance.acell('X6').value == "#DIV/0!"):
            team5Odds = placeholderReturn
        else:
            team5Odds = sheet_instance.acell('X6').value
        matchText = team1 + " vs " + team2 + " vs " + team3 + " vs " + team4 + " vs " + team5
    if(teams > 5):
        team6 = sheet_instance.acell('C4').value
        if(sheet_instance.acell('X7').value == "#DIV/0!"):
            team6Odds = placeholderReturn
        else:
            team6Odds = sheet_instance.acell('X7').value
        matchText = team1 + " vs " + team2 + " vs " + team3 + " vs " + team4 + " vs " + team5 + " vs " + team6
    
       

    for x in range(teams):
        try:
            num = int(sheet_instance.cell(x+2,25).value.replace(",",""))
            print("Num is " + str(num))
            if(num > 0):
                if(x==0):
                    underdog[0] = team1
                if(x==1):
                    underdog[1] = team2
                if(x==2):
                    underdog[2] = team3
                if(x==3):
                    underdog[3] = team4
                if(x==4):
                    underdog[4] = team5
                if(x==5):
                    underdog[5] = team6
                underdogBalance[x] = sheet_instance.cell(x+2,25).value
                print("Underdog spotted. Change in " + str(sheet_instance.cell(x+2,25).value))
                underdogExists = True
        except ValueError:
            print("Not a number")
            num = -1
        

    if(underdogExists):
        underdog = [i for i in underdog if i] 
        underdogBalance = [i for i in underdogBalance if i] 
        underText = ' \n '.join(map(str,underdog))
        underValue = ' \n '.join(map(str,underdogBalance))
        
    else:
        underText = "Currently No Underdog"
        underValue = "N/A"



    emb = discord.Embed(
        title = 'Now accepting bets for the following fight(s)!',
        description = matchText + '!',
        color = discord.Color.red()
    )

    
    emb.add_field(name= team1 + ' odds', value = '100k --> ' + team1Odds, inline=True)
    emb.add_field(name= team2 + ' odds', value = '100k --> ' + team2Odds, inline=True)
    emb.add_field(name= 'Current Underdog(s)', value = underText, inline=True)
    emb.add_field(name= team3 + ' odds', value = '100k --> ' + team3Odds, inline=True)
    emb.add_field(name= team4 + ' odds', value = '100k --> ' + team4Odds, inline=True)
    emb.add_field(name= 'Amount Till Change', value = underValue, inline=True)
    if(teams>4):
        emb.add_field(name= team5 + ' odds', value = '100k --> ' + team5Odds, inline=True)
    if(teams==6):
        emb.add_field(name= team6 + ' odds', value = '100k --> ' + team6Odds, inline=True)
    elif(teams == 5):
        emb.add_field(name='\u200b', value='\u200b',inline =True) 

    emb.add_field(name='\u200b', value='\u200b',inline =True) 

    await ctx.send(embed = emb)




bot.run(bot_key)