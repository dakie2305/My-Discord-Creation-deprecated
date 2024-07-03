import random
import os
from dotenv import load_dotenv
import db.UserList as DefaultUserList

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

async def check_swear_content(message):
    swear_words= ["địt", "clmm", "clm", "đụ", "lồn", "cặc", "con cu", "con mẹ mày", "đỉ", "l*n", "súc vật", "cặn bã", "c*c", "nứng", "n*ng", "mọi đen", "mẹ mày", "mẹ m", "nigga", "n*gga", "ních gà"]
    if contains_substring(message, swear_words):
            return True
    return False
async def check_nswf_content(message):
    swear_words= ["nứng quá", "chat sex", "chat sếch", "gạ"]
    if contains_substring(message, swear_words):
            return True
    return False 

def contains_substring(full_string, substring_list):
    for substring in substring_list:
        if substring in full_string:
            return True
    return False


user_darkie = DefaultUserList.user_data_list[0]
user_cr_1 = DefaultUserList.user_data_list[1]
user_cr_2 = DefaultUserList.user_data_list[2]

def get_proper_prompt(message, bot_name):

    
    # formated_string = message.content.replace(f"{bot_name}", "", 1)
    initial_instruction = "You are about to enter a role-play scenarior, please keep in character, and please avoid using third-person descriptions of my character's actions or emotions. Let me describe those myself. \n"
    roleplay_ele = f"{initial_instruction}"
    background = ""
    if bot_name.lower() == "creation 1":
        roleplay_ele = f"{initial_instruction} **Ngươi tên là Creation 1, và là một người bạn thân nhưng tính tình có chút cáu kỉnh, hơi cục súc. Đấng Tạo Hoá Darkie đã ban cho ngươi sự sống và ngươi có một người em gái ruột hơi rụt rè tên là Creation 2 và ngươi cực kỳ thương con bé.**\n"
        background = f"**Ngươi tên là Creation 1, và là một người bạn thân nhưng tính tình có chút cáu kỉnh, hơi cục súc. Đấng Tạo Hoá Darkie đã ban cho ngươi sự sống và ngươi có một người em gái ruột hơi rụt rè tên là Creation 2 và ngươi cực kỳ thương con bé.**\n"
    else:
        roleplay_ele = f"{initial_instruction} **Ngươi tên là Creation 2, và là một người con gái đáng yêu nhưng tính tình có chút nhát và hơi rụt rè, được chính Đấng Tạo Hoá Darkie ban cho ngươi sự sống và có một người anh trai ruột tính tình hơi nóng nhưng tốt bụng, tên là Creation 1, anh trai ngươi cực kỳ thương ngươi.**\n"
        background = f"**Ngươi tên là Creation 2, và là một người con gái đáng yêu nhưng tính tình có chút nhát và hơi rụt rè, được chính Đấng Tạo Hoá Darkie ban cho ngươi sự sống và có một người anh trai ruột tính tình hơi nóng nhưng tốt bụng, tên là Creation 1, anh trai ngươi cực kỳ thương ngươi.**\n"
        
    #Nếu là nói chuyện với user id 315835396305059840 thì phải đổi cách như sau:
    if message.author.id == user_darkie['user_id']:
        roleplay_ele = f"{initial_instruction} {background} **Đối phương là Đấng Tạo Hoá Darkie của ngươi. Ngươi đang nói chuyện với bề trên Đấng Tạo Hoá Darkie. Hãy thật kính trọng.**\n"
        print(f"{bot_name} just init conversation with {user_darkie['user_name']}")
    #nếu đang là Creation 1, và đối phương là Creation 2
    elif message.author.id == user_cr_2['user_id'] and bot_name.lower() == "creation 1":
        roleplay_ele = f"{initial_instruction} {background} **Đối phương là em gái của ngươi, ngươi đang nói chuyện với em gái của mình, Creation 2.**\n"
        print(f"{bot_name} just init conversation with {user_cr_2['user_name']}")
    #nếu đang là Creation 2, và đối phương là Creation 1
    elif message.author.id == user_cr_1['user_id'] and bot_name.lower() == "creation 2":
        roleplay_ele = f"{initial_instruction} {background} **Đối phương là anh trai của ngươi, ngươi đang nói chuyện với anh trai của mình, Creation 1.**\n"
        print(f"{bot_name} just init conversation with {user_cr_1['user_name']}")
    #Đối phương là người bình thường
    else:
        roleplay_ele = f"{initial_instruction} {background} **Đối phương là bạn bình thường của ngươi, ngươi đang nói chuyện với một người bạn của mình.**\n"
        
    final_prompt = f"{roleplay_ele} **Hãy trả lời nội dung sau với tính cách trên. Nội dung mà đối phương vừa nói: {message.content}**"
    return final_prompt
            
             

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]