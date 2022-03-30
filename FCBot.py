#Discord bot imports
import discord 
from discord.ext import commands

#Google sheet imports. Might need to be installed locally. Used this guide https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/
import gspread
from oauth2client.service_account import ServiceAccountCredentials


#Google Sheets Script Below
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('vhfc-bot-21b4604b07b0.json', scope)

client = gspread.authorize(creds)

sheet = client.open('VH Fight Club') #NAME OF SPREADSHEET OR URL

# Name of tab in spreedsheet
sheet_instance = sheet.worksheet('Fight Bookkeeping')

#Bot Script Below
bot = commands.Bot(command_prefix= '$')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Bets Closed!'))
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

@bot.command()
async def closed(ctx):
    await bot.change_presence(activity=discord.Game('Bets Closed!'))


@bot.command()
@commands.has_role("Fight Club Staff")
async def bets(ctx):
    await bot.change_presence(activity=discord.Game('Betting in Progress...'))
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
    if(sheet_instance.acell('X2').value > 0):
        team1Odds = sheet_instance.acell('X2').value
    else:
        team1Odds = 0
    team2 = sheet_instance.acell('B3').value
    if(sheet_instance.acell('X3').value > 0):    
        team2Odds = sheet_instance.acell('X3').value
    else:
        team2Odds = 0
    team3 = sheet_instance.acell('C2').value
    if(sheet_instance.acell('X4').value > 0):
        team3Odds = sheet_instance.acell('X4').value
    else:
        team3Odds = 0
    team4 = sheet_instance.acell('C3').value
    if(sheet_instance.acell('X5').value > 0):
        team4Odds = sheet_instance.acell('X5').value
    else:
        team4Odds = 0

    matchText = team1 + " vs " + team2 + " vs " + team3 + " vs " + team4
    if(teams > 4):
        team5 = sheet_instance.acell('B4').value
        team5Odds = sheet_instance.acell('X6').value
        matchText = team1 + " vs " + team2 + " vs " + team3 + " vs " + team4 + " vs " + team5
    if(teams > 5):
        team6 = sheet_instance.acell('C4').value
        team6Odds = sheet_instance.acell('X7').value
        matchText = team1 + " vs " + team2 + " vs " + team3 + " vs " + team4 + " vs " + team5 + " vs " + team6
    
       

    for x in range(teams):
        if((sheet_instance.cell(x+2,25).value != "0")):
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

    if(underdogExists):
        underdog = [i for i in underdog if i] 
        underdogBalance = [i for i in underdogBalance if i] 
        underText = ' | '.join(map(str,underdog))
        underValue = ' | '.join(map(str,underdogBalance))
        
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




bot.run('OTI0Nzc4MTk0NDE3MTIzMzQ4.Ycjgzw.WKcYPPOjipxRptsl7q9a4-tKVJg')