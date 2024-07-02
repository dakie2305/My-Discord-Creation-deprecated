# This example requires the 'message_content' intent.
import discord
import random
import os
from dotenv import load_dotenv

import pathlib
import textwrap

import google.generativeai as genai


load_dotenv()
def get_random_response(filename):
  """
  Đọc file .txt và trả về dòng ngẫu nhiên.

  Args:
      filename (str): Path to the text file.

  Returns:
      str: Chuỗi ngẫu nhiên, hoặc None nếu không có.
  """
  try:
    filepath = os.path.join(os.path.dirname(__file__),"Responses", filename)
    with open(filepath, 'r', encoding='utf-8') as f:
      lines = f.readlines()
      if lines:  # Check if there are any lines in the file
        return random.choice(lines).strip()  # lấy dòng ngẫu nhiên và strip string
      else:
        return None  # trả về None nếu file trống
  except FileNotFoundError:
    return None

def contains_substring(full_string, substring_list):
    for substring in substring_list:
        if substring in full_string:
            return True
    return False


intents = discord.Intents.default()
intents.message_content = True
API_KEY = os.getenv("GOOGLE_CLOUD_KEY")
genai.configure(api_key=API_KEY)

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # print(message)
    if message.author == client.user:
        return
    greetings = ["hello", "hi", "xin chào", "chào buổi", "ali", "alo"]
    bots_creation1_name = ["creation 1", "creation số 1", "creation no 1"]
    #Những điều cơ bản bình thường
    if contains_substring(message.content.lower(), greetings):
        response = get_random_response("OnGreeting.txt")
        formatted_response = response.replace("{message.author.mention}", message.author.mention)
        await message.channel.send(formatted_response)
        print(f'{message.author.mention} said Greeting so I greeted them')
     # Ai đó nhắc đến bot
    for mentioned_user in message.mentions:
        if mentioned_user == message.guild.me: 
            response = get_random_response("OnMentioned.txt")
            formatted_response = response.replace("{message.author.mention}", message.author.mention)
            await message.channel.send(formatted_response)
            print(f'{message.author.mention} mentioned me')
    if contains_substring(message.content.lower(), bots_creation1_name):
        model = genai.GenerativeModel('gemini-1.5-flash')
        formated_string = message.content.replace("Creation 1", "", 1)
        formated_string_2 = formated_string.replace("Creation 2", "", 1)
        response = model.generate_content(f"Hãy vờ như là một người bạn thân nhưng tính tình cáu kỉnh, hơi cục súc và trả lời: {formated_string_2}")
        # response = google_bard.generate_text(f"Hãy vờ như là một người bạn thân nhưng tính tình cáu kỉnh, hơi cục súc và trả lời: {message.content}", api_key=API_KEY)
        await message.channel.send(f"{message.author.mention} {response.text}")
        print("Someone directly call Creation 1")
        
    
bot_token = os.getenv("BOT_TOKENN")
client.run(bot_token)