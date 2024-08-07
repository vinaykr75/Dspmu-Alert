import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
from tinydb import TinyDB, Query
db = TinyDB('db.json')

User = Query()

bot_token = '6782568830:AAGORz9LYKqk4WjmTWKg2NDewPL8wsEHzEc'
chat_id = '-1002076457708'
application = Application.builder().token(bot_token).build()

proxy = {
   "http":"http://107.20.164.163:80"
}

url = 'https://www.dspmuranchi.ac.in/News.aspx'
headers = {
   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}


async def send_message(message_text):
    try:
       await application.bot.send_message(chat_id=chat_id, text=message_text,parse_mode="HTML")
       print("Message sent successfully!")
    except Exception as e:
         print(f"An error occurred:{e}")
         
async def main():    
 while True:
   notice_aar = [2867]
   title_nam = []
   link = []
   product = requests.get(url,headers=headers,proxies=proxy)
   soup = BeautifulSoup(product.text,features='lxml')
   table = soup.find('table', attrs={"class":"table"})
   td = table.find_all('a')
   curent_len = len(td)
   # db.insert({'total':curent_len,'id':'range'})
   
   for title in td:
      title_nam.append(title['title'])
      link.append('https://www.dspmuranchi.ac.in/'+title['href'].replace(' ','%20'))
   arry = db.search(User.id=='range')
   s = [sub['total'] for sub in arry]
   change_arry = s[0]
   # print(change_arry)

   if curent_len > change_arry:
    diff = curent_len - change_arry
    for i in range(0 , diff):
      # print(title_nam[i])
      # print(link[i])
      message_text = f'<b>{title_nam[i]}</b>\n<a href="{link[i]}">Download Notice</a>'
      await send_message(message_text) 
   db.update({'total':curent_len},User.id == 'range')
 
if __name__ == "__main__":
    asyncio.run(main())