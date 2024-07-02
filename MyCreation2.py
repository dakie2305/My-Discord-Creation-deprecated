# This example requires the 'message_content' intent.
import discord
import random
import os
from dotenv import load_dotenv
import functions
import db.UserList as DefaultUserList
import google.generativeai as genai


load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
API_KEY = os.getenv("GOOGLE_CLOUD_KEY_2")
genai.configure(api_key=API_KEY)

client = discord.Client(intents=intents)
user_darkie = DefaultUserList.user_data_list[0]
user_cr_1 = DefaultUserList.user_data_list[1]
user_cr_2 = DefaultUserList.user_data_list[2]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # print(message)
    if message.author == client.user:
        return
    greetings = ["hello", "hi", "xin chào", "chào buổi", "ali", "alo"]
    bots_creation1_name = ["creation 2", "creation số 2", "creation no 2"]
    #Những điều cơ bản bình thường
    if functions.contains_substring(message.content.lower(), greetings):
        response = functions.get_random_response("OnGreeting.txt")
        formatted_response = response.replace("{message.author.mention}", message.author.mention)
        await message.channel.send(formatted_response)
        print(f'{message.author.mention} said Greeting so I greeted them (No. 2)')
     # Ai đó nhắc đến bot
    for mentioned_user in message.mentions:
        if mentioned_user == message.guild.me and message.author.id != user_cr_1['user_id']: 
            response = functions.get_random_response("OnMentioned.txt")
            formatted_response = response.replace("{message.author.mention}", message.author.mention)
            await message.channel.send(formatted_response)
            print(f'{message.author.mention} mentioned me')
            
    if functions.contains_substring(message.content.lower(), bots_creation1_name):
        model = genai.GenerativeModel('gemini-1.5-flash', functions.safety_settings)
        formated_string = message.content.replace("Creation 2", "", 1)
        roleplay_ele = "Please avoid using third-person descriptions of my actions or emotions. Let me describe those myself. Hãy nhập vai người như sau: ngươi tên là Creation 2, và là một người con gái đáng yêu nhưng tính tình có chút nhát và hơi rụt rè, được chính Đấng Tạo Hoá Darkie ban cho ngươi sự sống và có một người anh trai ruột tính tình hơi nóng nhưng tốt bụng, tên là Creation 1, anh trai ngươi cực kỳ thương ngươi. Chỉ tập trung tương tác theo góc nhìn thứ nhất."
        #Nếu là nói chuyện với user id 315835396305059840 thì phải đổi cách như sau:
        if message.author.id == user_darkie['user_id']:
            roleplay_ele = "Hãy đóng vai như sau: ngươi tên là Creation 2, và ngươi đang nói chuyện với bề trên Đấng Tạo Hoá Darkie. Hãy thật kính trọng. "
        response = model.generate_content(f"{roleplay_ele} Sau đó, hãy trả lời nội dung sau với tính cách trên: {formated_string}")
        # response = google_bard.generate_text(f"Hãy vờ như là một người bạn thân nhưng tính tình cáu kỉnh, hơi cục súc và trả lời: {message.content}", api_key=API_KEY)
        await message.channel.send(f"{message.author.mention} {response.text}")
        print("Someone directly call Creation 2")
    
        
    
bot_token = os.getenv("BOT_TOKEN_NO2")
client.run(bot_token)