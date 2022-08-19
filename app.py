from ast import expr_context
from dataclasses import fields
import json
from turtle import title
from typing import ItemsView
import interactions
from aiocfscrape import CloudflareScraper as requests
import asyncio
from functools import wraps
#Decorator to check if the moon access is expired and notify user to update it 
def unauthorized(func):
    async def wrapper(*a,**k):
        try:
            fuc =  await func(*a,**k)
            return fuc
        except Exception as ex:
            embed = interactions.Embed(title=":x: Unauthorized",color=15158332,description= "Moon access token is expired / invaild, please update it with ``/setup`` command")

            await a[0].send(embeds=embed)
            
    return  wrapper

class Moon:
    def __init__(self,token) -> None:
        if token != "":
            self.access_token = token
        self.authed=True
        self.base = "https://api.paywithmoon.com/v1/moon/" 
        
    # making requests session & adding headers to it 
    async def init_session(self,token=None):
            if token == None:
                token = self.access_token
            self.headers = {
  'authority': 'api.paywithmoon.com',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9',
  'authorization': 'Bearer '+token,
  'content-type': 'application/json; charset=UTF-8',
  'origin': 'https://paywithmoon.com',
  'referer': 'https://paywithmoon.com/',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'
}
            self.session = requests()
            for key,val in self.headers.items():
                self.session.headers.add(key,val)
    #making requests to base url of moon api
    async def __request(self,method:str,path,posted_data=None):
        if posted_data == None:
            resp = await self.session.request(method,self.base+path,headers=self.headers)
        else:
            resp = await self.session.request(method,self.base+path,headers=self.headers,json=posted_data)
        # checking of moon access token is valid
        if resp.status == 401:
            raise Exception('auth')
        else:
            try:
                return await  resp.json()
            except:
                print(resp.text)
    
    async def delete_card(self,card_id):
        resp = await self.__request("post","cards/delete",{"comments":"","cardId":card_id,"platform":"web-app"})
    async def get_profile(self):
        try:
            response = await self.__request("GET","users?includeCoinbaseInfo=false")
            return True, response['user']
        except:
            return False,None
    async def generate_card(self,amount=5):
        suc , card =await self.get_active_card()
        if suc:
            await self.delete_card(card)
        response = await self.__request('POST',"getdepositaddress",{"amount":f"{amount}.00","applyRewardSats":False,"applyUsdCredit":True,"cardProduct":"CREDIT_CARD_PRODUCT"})
        try:
            response = response['card']
            return True,response["pan"] , response["exp"][:2] + "/" + response["exp"][2:],response["cvv"],response['expirationTime']
        except:
            return [True,None , None,None,None]
    # @is_authed
    async def get_transactions(self):
        resp = await self.__request('post',"transactions?currentPage=1&perPage=10")
        return resp
    # @is_authed
    async def get_active_card(self):
        resp = await self.__request('get',"cards?display=&currentPage=1&perPage=1&inactiveCards=false")
        try:
            card = resp["cards"][0]['id']
            return True,card
        except:
            return False,None
config = json.load(open('config.json'))
bot = interactions.Client(config['bot_access_token'])

moon =  Moon(config['moon_access_token'])
@bot.command(
name='setup',
description='set you moon account access token',
options=[interactions.Option(name="token",description="your moon access token",required=True,type=interactions.OptionType.STRING)]
)
async def setup(ctx:interactions.CommandContext,token):
    moon.access_token = token
    await moon.init_session(token)
    try:
        s,profile = await moon.get_profile()
        embed = interactions.Embed(title=":white_check_mark: token saved")
        embed.add_field("name",profile['name'])
        embed.add_field('email',profile['email'])
        embed.add_field('balance',profile['credit'])
        config["moon_access_token"] = token
        json.dump(config,open('config.json','w'))
        await ctx.send(embeds=embed)
    except Exception as ex:
        await ctx.send(embeds=interactions.Embed(title=":x: invaild moon token!",color=15158332))

@bot.command(
    name="transactions",
    description="get your last 10 transaction"
)
@unauthorized
async def transactions(ctx:interactions.CommandContext):
    await moon.init_session()
    trans = await moon.get_transactions()
    trans = list(trans['transactions'])
    for trx in trans:
        embed = interactions.Embed(color=3066993,title=f":money_with_wings: Transaction #{trans.index(trx)}")
        embed.add_field('Type',trx['type'])
        trx = dict(trx['data'])
        for key,val in trx.items():
            embed.add_field(key,val,inline=True)
        await ctx.send(embeds=embed)

@bot.command(
    name="generate",
    description="Generate A vcc for you",
    options=[
        interactions.Option(
            name="amount",
            required=False,
            description="Card Load Amount",
            type = interactions.OptionType.INTEGER
        )
    ]
)
@unauthorized
async def generate(ctx:interactions.CommandContext,amount:int = 5):
    await moon.init_session()
    success,pan,exp,cvv,exptime = await moon.generate_card(amount)
    if success:
        embed = interactions.Embed(title=":white_check_mark: Vcc generated successfully",color=3066993,description="your card is ready",
                        fields=[
        interactions.EmbedField(name="Pan",value=pan),
        interactions.EmbedField(name="Exp",value=exp),
        interactions.EmbedField(name="Cvv",value=cvv),
        interactions.EmbedField(name="Expiration time",value=exptime)
        ]
        )
        
    else:
        embed = interactions.Embed(title=":x: Error",color=15158332,description= "it seems like you don't have enoght balance")
    await ctx.send(embeds=embed)
@bot.event
async def on_ready():
    print(bot.me.name," is ready . ")
bot.start()
