#Clean This Up
#---------------------------------------------------------------------------
from __future__ import print_function, unicode_literals
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import urllib3
from bs4 import BeautifulSoup
import os.path
from os import system, name
from time import sleep
from json import JSONDecoder
from functools import partial
from pyfiglet import Figlet

from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
#---------------------------------------------------------------------------

#Sleep Timer
i = 10

#Screen Clear | For Windows use 'cls'
def clear():
  
    system('clear')

#JSON Parse Buffer
def json_miner(fileobj, decoder=JSONDecoder(), buffersize=2048):
    buffer = ''
    for chunk in iter(partial(fileobj.read, buffersize), ''):
         buffer += chunk
         while buffer:
             try:
                 result, index = decoder.raw_decode(buffer)
                 yield result
                 buffer = buffer[index:]
             except ValueError:
                 # Not enough data to decode, read more
                 break

#Main Program
def Main():

	#Opening Text
	f = Figlet(font='slant')
	print (f.renderText('Mission Command'))

	#Console Style
	style = style_from_dict({
	    Token.Separator: '#cc5454',
	    Token.QuestionMark: '#673ab7 bold',
	    Token.Selected: '#cc5454',  # default
	    Token.Pointer: '#673ab7 bold',
	    Token.Instruction: '',  # default
	    Token.Answer: '#f44336 bold',
	    Token.Question: '',
	})

	#Input API Key
	API = [
	    {
	        'type': 'input',
	        'name': 'API',
	        'message': 'CoinMarketCap API Key',
	    }
	    ]

	#Input Coin Name
	questions = [
	    {
	        'type': 'input',
	        'name': 'Coin',
	        'message': 'Coin/Token Name (All Caps)',
	    }
	    ]

	#Coin Parameter Checkboxes
	questions2 = [
	            {

	        'type': 'checkbox',
	        'message': 'Select Token/Coin Parameters',
	        'name': 'dataReq',
	        'choices': [
	            Separator('= Parameters ='),
	            {
	                'name': 'price',
	            },
	            {
	                'name': 'change'
	            },
	            {
	                'name': 'volume'
	            },
	            Separator('= Metrics ='),
	            {
	                'name': 'MarketCap'
	            },
	            {
	                'name': 'TotalSupply'
	            },
	            {
	                'name': 'Circulating'
	            },
	            Separator('= Enviornment ='),
	            {
	                'name': 'Platform'
	            },
	            {
	                'name': 'ContractAddress',
	            },
	            {
	                'name': 'Rank'
	            }
	        ],
	        'validate': lambda answer: 'You must choose at least one variable' \
	            if len(answer) == 0 else True
	    }
	]

	#Format Answers
	apiKey = prompt(API, style=style)
	answers = prompt(questions, style=style)
	answers2 = prompt(questions2, style=style)
	#pprint(answers)
	#pprint(answers2)

	#Convert Answers
	json_Api = json.dumps(apiKey,sort_keys=True,indent=2)
	json_Answer = json.dumps(answers,sort_keys=True,indent=2)
	json_Answers = json.dumps(answers2,sort_keys=True,indent=2)

	#Load 'Coin' Varible
	json_Answer_Var = json.loads(json_Answer)
	coin = json_Answer_Var['Coin']

	#Load 'API' Varible
	json_Api_Var = json.loads(json_Api)
	cmcApi = json_Api_Var['API']

	#print (coin)

	#API URL
	url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
	parameters = {
	  'symbol':''+str(coin)+'',
	  'convert':'USD'
	}

	#API Headers & Key
	headers = {
	  'Accepts': 'application/json',
	  'X-CMC_PRO_API_KEY': ''+str(cmcApi)+'',
	}

	#API Session
	session = Session()
	session.headers.update(headers)
	response = session.get(url, params=parameters)

	#Data Conversion & Offline File Store
	data1 = json.loads(response.text)
	json_string = json.dumps(data1,sort_keys=True,indent=2)

	f = open('data.txt', 'w')
	f.write(json_string)
	with open('data.txt', 'rb') as f:
	    byte = f.read()
	byte
	f.close()
	with open('data.txt', 'r') as order:
	  	for data in json_miner(order):
	  		json_string = json.dumps(data,sort_keys=True,indent=2)
	  		data = json.loads(json_string)
	  		#print (json_string)
	  		#print (data)
	  		pairs = data.items()

	#Loop To Display Data
	def Release():
		while True:
			try:
				if 'price' in json_Answers:
					for key, value in pairs:
			  			print(' Price: ',value[''+str(coin)+'']['quote']['USD']['price'])
			  			sleep(i)
			  			clear()
			  			Main()
				elif 'change' in json_Answers:
			  		for key, value in pairs:
			  			print(' 24Hr Change: ',value[''+str(coin)+'']['quote']['USD']['percent_change_24h'])
			  			sleep(i)
			  			clear()
			  			Main()
				elif 'volume' in json_Answers:
			  		for key, value in pairs:
			  			print(' Volume: ',value[''+str(coin)+'']['quote']['USD']['volume_24h'])
			  			sleep(i)
			  			clear()
			  			Main()
				elif 'MarketCap' in json_Answers:
			  		for key, value in pairs:
			  			print(' Market Cap: ',value[''+str(coin)+'']['quote']['USD']['market_cap'])
			  			sleep(i)
			  			clear()
			  			Main()
				elif 'TotalSupply' in json_Answers:
			  		for key, value in pairs:
			  			print(' Total Supply: ',value[''+str(coin)+'']['total_supply'])
			  			sleep(i)
			  			clear()
			  			Main()
				elif 'Circulating' in json_Answers:
			  		for key, value in pairs:
			  			print(' Circulating Supply: ',value[''+str(coin)+'']['circulating_supply'])
			  			sleep(i)
			  			clear()
			  			Main()
				elif 'Platform' in json_Answers:
			  		for key, value in pairs:
			  			print(' Platform: ',value[''+str(coin)+'']['platform']['name'])
			  			sleep(i)
			  			clear()
			  			Main()
				elif 'ContractAddress' in json_Answers:
			  		for key, value in pairs:
			  			print(' Token Address: ',value[''+str(coin)+'']['platform']['token_address'])
			  			sleep(i)
			  			clear()
			  			Main()
				elif 'Rank' in json_Answers:
			  		for key, value in pairs:
			  			print(' CMC-Rank: ',value[''+str(coin)+'']['cmc_rank'])
			  			sleep(i)
			  			clear()
			  			Main()
				elif 'null' in data:
			  		print ('Null: ', data['null'])
				else:
			  		print('Error')
			  		break
			except:
				clear()
				Main()
			 	#print ("EXCEPTION: Error - Dumping Data >> ", data)
	Release()
clear()
Main()
