# This example requires the 'message_content' intent.
import discord
import random
import os
from dotenv import load_dotenv

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