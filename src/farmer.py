import discord
import asyncio
import bs4 as bs
import urllib.request
from selenium import webdriver
from tabulate import tabulate
from discord.ext.commands import Bot
from discord.ext import commands

# Using seleinum to click on farm list and start reload it.
# No browser, No problem lets use binaries :)

master_site = "https://www.travian.com/us"
SERVER = "ts3.travian.us"
stats_headers = ['#', 'Player', 'Alliance', 'Villages', 'Conquest', 'Population']

Client = discord.Client() #Initialise Client 
client = commands.Bot(command_prefix = "!") #Initialise client bot

#uses selenium to load page as bs4 only works on static page.
def get_source(url):
	browser = webdriver.Firefox(executable_path=r"../bin/geckodriver")
	browser.get(url)
	html = browser.page_source
	browser.close()
	return html


def days ():
	html_src = get_source(master_site+"?server=us3#register");
	soup = bs.BeautifulSoup(html_src, "lxml")
	word_div = soup.find("div", { "class" : "world default"})
	spans = word_div.find_all("span");
	day=""
	for span in spans:
		day+= span.string+' ';
	return day;

def stats():
	sauce = urllib.request.urlopen("https://www.gettertools.com/ts3.travian.us.7/10-Travian-world").read()
	soup = bs.BeautifulSoup(sauce,"lxml")
	tables = soup.find_all("table", {"class" : "cs0 nowrap"});
	return tableSummary(tables[0]);
	
def tableSummary(table):
	trs = table.find_all('tr')
	summary = ""
	for tr in trs:
		td = tr.find_all('td')
		row = [i.text for i in td]
		summary += ' '.join(row)
		summary+='\n'
	return summary

def process_tr(table_tr):
	new_table = []
	for tr in table_tr[3:18]:
		del tr[len(tr)-1]
		tr[3] = tr[3] + tr[4]
		del tr[4]
		tr[4] = tr[4] + tr[5]
		del tr[5]
		tr[5] = tr[5] + tr [6]
		del tr[6]
		tr[0] = tr[0].replace(".","")
		new_table.append(tr)
	return new_table

def top15(tribe):
	sauce = urllib.request.urlopen("https://www.gettertools.com/ts3.travian.us.7/11.4-Tribes-separated").read()
	soup = bs.BeautifulSoup(sauce,"lxml")
	tables = soup.find_all("table",{"class" : "orangeTable"});
	table = None
	if tribe == 'romans':
		table =tables[0]

	elif tribe == 'teutons':
		table =tables[1]

	elif tribe == 'gauls':
		table =tables[2]

	table_tr =[]
	trs = table.find_all('tr')
	for tr in trs:
		td = tr.find_all('td')
		row = [i.text for i in td]
		table_tr.append(row)

	table_tr = process_tr(table_tr)
	return tabulate(table_tr, stats_headers)

def top_pop():
	sauce = urllib.request.urlopen("https://www.gettertools.com/ts3.travian.us.7/10-Travian-world").read()
	soup = bs.BeautifulSoup(sauce,"lxml")
	tables = soup.find_all("table",{"class" : "orangeTable"});
	table = tables[0]
	table_tr =[]
	trs = table.find_all('tr')
	for tr in trs:
		td = tr.find_all('td')
		row = [i.text for i in td]
		table_tr.append(row)
	table_tr = process_tr(table_tr)
	return tabulate(table_tr,stats_headers)


@client.event 
async def on_ready():
    print("Bot is online and connected to Discord") 

  
@client.event
async def on_message(message):
    if message.content.startswith('!top15'):
	    msg = top_pop()
	    await client.send_message(message.channel, msg)

    elif message.content.startswith('!romans'):
	    msg = top15('romans')
	    await client.send_message(message.channel, msg)

    elif message.content.startswith('!gauls'):
	    msg = top15('gauls')
	    await client.send_message(message.channel, msg)

    elif message.content.startswith('!teutons'):
	    msg = top15('teutons')
	    await client.send_message(message.channel, msg)

    elif message.content.startswith('!info'):
	    msg = days()
	    await client.send_message(message.channel, msg)

    elif message.content.startswith('!stats'):
	    msg = stats()
	    await client.send_message(message.channel, msg)

client.run("YourToken")
