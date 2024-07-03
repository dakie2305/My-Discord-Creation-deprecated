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


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # print(message)
    if message.author == client.user:
        return
    greetings = ["hello", "hi", "xin chào", "chào buổi", "ali", "alo"]
    bots_creation_name = ["creation 2", "creation số 2", "creation no 2"]
    #Những điều cơ bản bình thường
         # Cần cải thiện lại
    # if functions.contains_substring(message.content.lower(), greetings):
    #     response = functions.get_random_response("OnGreeting.txt")
    #     formatted_response = response.replace("{message.author.mention}", message.author.mention)
    #     await message.channel.send(formatted_response)
    #     print(f'{message.author.mention} said Greeting so I greeted them (No. 2)')
    stop_flag = False
    #Ai đó nhắc đến bot
    for mentioned_user in message.mentions:
        if mentioned_user == message.guild.me and message.author.id != functions.user_cr_1['user_id']: 
            response = functions.get_random_response("OnMentioned.txt")
            formatted_response = response.replace("{message.author.mention}", message.author.mention)
            await message.channel.send(formatted_response)
            print(f'{message.author.mention} mentioned me')
            
    if functions.contains_substring(message.content.lower(), bots_creation_name):
        while(stop_flag != True):
            #Kiểm tra message swear words
            check_swear_words = await functions.check_swear_content(message.content.lower())
            if check_swear_words:
                response = functions.get_random_response("OnSwearWords.txt")
                formatted_response = response.replace("{message.author.mention}", message.author.mention)
                await message.channel.send(formatted_response)
                print(f"Username {message.author.name}, Display user name {message.author.display_name}, just use swear word at {client.user}")
                stop_flag = True
                break
            
            #Kiểm tra message nsfw
            check_nsfw_words = await functions.check_nswf_content(message.content.lower())
            if check_nsfw_words:
                response = functions.get_random_response("OnHornyWords.txt")
                formatted_response = response.replace("{message.author.mention}", message.author.mention)
                await message.channel.send(formatted_response)
                print(f'{message.author.mention} just use nsfw at {client.user}')
                stop_flag = True
                break
            
            roles_of_user = message.author.roles
            for role in roles_of_user:
                if role.name == "Đáy Xã Hội":
                    #Role bị khinh bỉ
                    response = functions.get_random_response("OnDespitedRole.txt")
                    formatted_response = response.replace("{message.author.mention}", message.author.mention)
                    await message.channel.send(formatted_response)
                    print(f"{client.user} just despited Username {message.author.name}, Display user name {message.author.display_name}")
                    stop_flag = True
                    break
            break
        
        if stop_flag == False:
            model = genai.GenerativeModel('gemini-1.5-flash', functions.safety_settings)
            prompt = functions.get_proper_prompt(message,"Creation 2")
            print(f"Prompt generated from {client.user}: {prompt}")
            response = model.generate_content(f"{prompt}")
            await message.channel.send(f"{message.author.mention} {response.text}")
            print(f"Username {message.author.name}, Display user name {message.author.display_name} directly call {client.user}")
    
    
bot_token = os.getenv("BOT_TOKEN_NO2")
client.run(bot_token)