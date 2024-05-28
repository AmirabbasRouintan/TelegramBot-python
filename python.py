 #  _         _                              _   _     _                            ____ ____ ____ 
 # (_)_ _  __| |_ __ _ __ _ _ _ __ _ _ __   (_) (_)_ _(_)  _____ ___ ____ _ __ _ __|__  |__  |__  |
 # | | ' \(_-<  _/ _` / _` | '_/ _` | '  \   _  | \ \ / | (_-< _` \ V / _` / _` / -_)/ /  / /  / / 
 # |_|_||_/__/\__\__,_\__, |_| \__,_|_|_|_| (_) |_/_\_\_|_/__|__,_|\_/\__,_\__, \___/_/  /_/  /_/  
 #                    |___/                            |___|               |___/                   

# import telebot

# bot = telebot.TeleBot("----------------------- your telebot api -----------------------")

# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
# 	bot.reply_to(message, "Howdy, how are you doing?")

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
# 	bot.reply_to(message, message.text)

# bot.infinity_polling()

# ==========================================================================# ==========================================================================# ==========================================================================# ==========================================================================
# ==========================================================================# ==========================================================================# ==========================================================================
# ==========================================================================# ==========================================================================

import cv2
import time
from pyngrok import ngrok
import requests
import os
import psutil
import time
import sys
import subprocess
import random
import csv
import json
import datetime
import telebot
from telebot import types
import pyautogui

banned_users_csv_path = 'banned_users.csv'
bot = telebot.TeleBot("----------------------- your telebot api for ex : 6983934985792:AAGF6EHZjYxsdfglskdfglXuH4oICYwhlo13ME -----------------------")

try:
    with open('usernames.json', 'r') as json_file:
        usernames = json.load(json_file)
except FileNotFoundError:
    usernames = {}

user_id_counter = 1

banned_users = set()

def save_banned_users_to_csv():
    with open(banned_users_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['user_id', 'username']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for user_id in banned_users:
            try:
                user_info = bot.get_chat_member(chat_id, user_id)
                username = user_info.user.username
            except Exception as e:
                print(f"Error getting username: {e}")
                username = f"user_id_{user_id}"

            writer.writerow({'user_id': user_id, 'username': username})

def load_banned_users_from_csv():
    try:
        with open(banned_users_csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = int(row['user_id'])
                banned_users.add(user_id)
    except FileNotFoundError:
        print("No previous ban list found.")

# Define the /start command handler
@bot.message_handler(commands=['start'])
def send_username(message):
    if message.from_user.username == '<your telegram username>':
        bot.reply_to(message, f"👋 Hello, ✨Boss\n\nWelcome to your Chat 👀💖")
    else: 
        if message.from_user.username:
            username = message.from_user.username
            bot.reply_to(message, f"👋 Hello, @{username}\n\nwelcome to this bot \nthis bot it isn't done yet :)")
        else:
            bot.reply_to(message, "👋 Hi, welcome\nYou don't have a Telegram username?") 

@bot.message_handler(commands=['help'])
def send_help_text(message):
    bot.reply_to(message, "1. /username\n2. /pic\n\nUntil now :) ")

# Define the /pic command handler
@bot.message_handler(commands=['pic'])
def send_pic_text(message):
    bot.reply_to(message, "Pics avb :\n\n1. /pic1\n2. /piv2")

# Define the /pic1 command handler
@bot.message_handler(commands=['pic1'])
def send_image(message):
    bot.reply_to(message, "🔴 Wait ....")
    try:
        with open('pic1.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except Exception as e:
        print(f"Error sending image: {e}")

# Define the /username command handler
@bot.message_handler(commands=['username'])
def ask_for_name(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Please type your name:", reply_markup=markup)

load_banned_users_from_csv()

# Define the /kick command handler
@bot.message_handler(commands=['kick'])
def kick_user(message):
    if message.from_user.username == '<your telegram username>':
        if message.reply_to_message and message.reply_to_message.from_user:
            user_id = message.reply_to_message.from_user.id
            chat_id = message.chat.id

            bot.kick_chat_member(chat_id, user_id)

            bot.reply_to(message, f"User {user_id} has been kicked from the group.")
        else:
            bot.reply_to(message, "boss😎, Please reply to a message to specify the user to kick.🙌")
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

# ban
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.username == '<your telegram username>':
        chat_id = message.chat.id  # Define chat_id here

        if message.reply_to_message and message.reply_to_message.from_user:
            user_id = message.reply_to_message.from_user.id

            bot.restrict_chat_member(chat_id, user_id, can_send_messages=False)

            banned_users.add(user_id)

            bot.reply_to(message, f"🟥User {user_id} has been banned from sending messages in the group.")
            save_banned_users_to_csv()
        else:
            entities = message.entities or message.caption_entities
            if entities:
                for entity in entities:
                    if entity.type == 'mention':
                        mention_offset = entity.offset
                        mention_length = entity.length
                        mentioned_username = message.text[mention_offset + 1: mention_offset + mention_length]

                        # Get user info by username
                        try:
                            user_info = bot.get_chat_member(chat_id, mentioned_username)
                            user_id = user_info.user.id

                            bot.restrict_chat_member(chat_id, user_id, can_send_messages=False)

                            banned_users.add(user_id)

                            bot.reply_to(message, f"🔴 User {user_id} ({mentioned_username}) has been banned from sending messages in the group.")
                            save_banned_users_to_csv()
                            return

                        except Exception as e:
                            bot.reply_to(message, f"Error banning user: {e}")
                            return

            bot.reply_to(message, "Please reply to a message.")
    else:
        bot.reply_to(message, "🔴You are not boss to use this command.👿")

# Define the /unban command handler
@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.from_user.username == '<your telegram username>':
        if banned_users:
            markup = types.ReplyKeyboardMarkup(row_width=1, selective=True)
            for user_id in banned_users:
                try:
                    user_info = bot.get_chat_member(message.chat.id, user_id)  # Pass message.chat.id here
                    username = user_info.user.username
                    markup.add(types.KeyboardButton(f'Unban @{username} ({user_id})'))
                except Exception as e:
                    print(f"Error getting username: {e}")
                    markup.add(types.KeyboardButton(f'Unban user_id_{user_id}'))

            bot.send_message(message.chat.id, "Select a user to unban:", reply_markup=markup)  # Pass message.chat.id here
        else:
            bot.reply_to(message, "👀🤔There are no banned users.")
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

@bot.message_handler(func=lambda message: message.text.startswith('Unban'))
def handle_unban_click(message):
    if message.from_user.username == '<your telegram username>':
        chat_id = message.chat.id
        user_id_to_unban = int(message.text.split('(')[1].split(')')[0])

        try:
            user_info = bot.get_chat_member(chat_id, user_id_to_unban)
            username_to_unban = user_info.user.username
        except Exception as e:
            print(f"Error getting username: {e}")
            username_to_unban = f"user_id_{user_id_to_unban}"

        bot.restrict_chat_member(chat_id, user_id_to_unban, can_send_messages=True)
        banned_users.remove(user_id_to_unban)

        save_banned_users_to_csv()

        bot.reply_to(message, f"User @{username_to_unban} ({user_id_to_unban}) has been unbanned🎉. They can now send messages in the group.😊")
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

def capture_photo(camera_index=0, photo_filename='captured_photo.jpg'):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        cap.release()
        return None

    cv2.imwrite(photo_filename, frame)

    cap.release()
    print(f"Photo captured and saved as {photo_filename}")
    return photo_filename

@bot.message_handler(commands=['takephoto'])
def take_photo(message):
    if message.from_user.username == '<your telegram username>' :
        photo_filename = capture_photo()

        if photo_filename:
            with open(photo_filename, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.reply_to(message, "Failed to capture the photo. Please try again.")
    else : 
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

spam_messages = {}

@bot.message_handler(commands=['spam'])
def start_spam(message):
    if message.from_user.username == '<your telegram username>':
        user_id = message.from_user.id
        markup = types.ForceReply(selective=False)
        bot.reply_to(message, "Sure, sir. Please specify the message you want to spam:", reply_markup=markup)
        bot.register_next_step_handler(message, get_spam_message, user_id)
    else : 
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")
        

def get_spam_message(message, user_id):
    if message.from_user.username == '<your telegram username>':
        spam_message = message.text
        if not spam_message.startswith('/stopspam'):
            spam_messages[user_id] = spam_message
            bot.reply_to(message, f"Spam message set. To start spamming, use the command: /startspam")
        else:
            bot.reply_to(message, "Spam command canceled.")
    else : 
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")
        

@bot.message_handler(commands=['startspam'])
def start_spamming(message):
    if message.from_user.username == '<your telegram username>':
        user_id = message.from_user.id
        if user_id in spam_messages:
            spam_message = spam_messages[user_id]
            bot.reply_to(message, "Spamming started. To stop, use the command: /stopspam")
            while True:
                bot.send_message(message.chat.id, spam_message)
                time.sleep(1)
                if user_id not in spam_messages:
                    break
        else:
            bot.reply_to(message, "No spam message set. Use /spam to set a message.")
    else : 
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

@bot.message_handler(commands=['stopspam'])
def stop_spamming(message):
    if message.from_user.username == '<your telegram username>':
        user_id = message.from_user.id
        if user_id in spam_messages:
            del spam_messages[user_id]
            if user_id in spam_processes:
                spam_process = spam_processes[user_id]
                spam_process.terminate()
                del spam_processes[user_id]
                bot.reply_to(message, "Spamming stopped.")
            else:
                bot.reply_to(message, "No active spamming processes found.")
        else:
            bot.reply_to(message, "No active spamming sessions found.")
    else : 
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

# List of jokes
jokes = [
    "Why did the math book look sad? Because it had too many problems.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "How does a penguin build its house? Igloos it together.",
    "I used to play piano by ear, but now I use my hands and fingers.",
    "Why don't oysters donate to charity? Because they are shellfish.",
    "What did one hat say to the other? Stay here, I'm going on ahead!",
    "I only know 25 letters of the alphabet. I don't know y.",
    "Why did the scarecrow become a successful motivational speaker? He was outstanding in his field.",
    "I told my computer I needed a break, and now it won't stop sending me vacation ads. It's not listening.",
    "How do you organize a fantastic space party? You planet well in advance."
    "Why don't scientists trust atoms? Because they make up everything!",
    "Did you hear about the mathematician who's afraid of negative numbers? He will stop at nothing to avoid them.",
    "How do you organize a space party? You planet.",
    "I told my wife she should embrace her mistakes. She gave me a hug.",
    "Why don't skeletons fight each other? They don't have the guts.",
    "What's orange and sounds like a parrot? A carrot.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "I told my computer I needed a break, and now it won't stop sending me vacation ads.",
    "Why did the bicycle fall over? Because it was two-tired.",
    "Parallel lines have so much in common. It's a shame they'll never meet."
    "Why don't scientists trust atoms? Because they make up everything.",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
]

@bot.message_handler(commands=['joke'])
def send_joke(message):
    if jokes:
        random_joke = random.choice(jokes)
        bot.reply_to(message, random_joke)
    else:
        bot.reply_to(message, "Sorry, no jokes available at the moment.")

# Define the /exit command handler
@bot.message_handler(commands=['exit'])
def exit_bot(message):
    if message.from_user.username == '<your telegram username>':
        save_banned_users_to_csv()
        bot.reply_to(message, "🟥Bot is exiting. Banned users list has been saved.😢")
        exit()
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

@bot.message_handler(commands=['pin'])
def pin_message(message):
    if message.reply_to_message:
        bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        bot.reply_to(message, "🔴Message has been pinned bro 😊")
    else:
        bot.reply_to(message, "Please reply to a message to use /pin.")

# say welcome to new users :) < - - 
@bot.message_handler(content_types=['new_chat_members'])
def handle_new_chat_members(message):
    for member in message.new_chat_members:
        bot.reply_to(message, f"🟥 Welcome🙌, {member.first_name} \nWelcome to you chat 😊\nI'm IXI_bot and I help the user to do thire work better 🤸‍♀️👌")

# Define the /gif command handler
@bot.message_handler(commands=['gif'])
def send_pic_text(message):
    bot.reply_to(message, "🌟all of your gif boss✨\n👿list of the gif:\n\n/gif1\n/gif2\n/gif3\n/gif4\n/gif5\n/gif6\n\n😇good gif : \n\n/gif7\n/gif8\n/gif9\n/gif10")


# @bot.message_handler(commands=['gif'])
# def send_gif_list(message):
#     gif_list_message = bot.reply_to(message, "🌟all of your gif boss✨\n👿list of the gif:\n\n/gif1\n/gif2\n/gif3\n/gif4\n/gif5\n/gif6\n\n😇good gif : \n\n/gif7\n/gif8\n/gif9\n/gif10")

#     # Sleep for 5 seconds
#     time.sleep(5)

#     # Delete the original message
#     bot.delete_message(chat_id=message.chat.id, message_id=gif_list_message.message_id)

# ==============

# Define the /gif1 command handler
@bot.message_handler(commands=['gif1'])
def send_custom_gif1(message):
    if message.from_user.username == '<your telegram username>':
        bot.reply_to(message, "🔴 Wait ....")
        with open('python_gif\gif1.gif', 'rb') as gif:
            bot.send_document(message.chat.id, gif)
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

# Define the /gif2 command handler
@bot.message_handler(commands=['gif2'])
def send_custom_gif2(message):
    if message.from_user.username == '<your telegram username>':
        bot.reply_to(message, "🔴 Wait ....")
        with open('python_gif\gif2.gif', 'rb') as gif:
            bot.send_document(message.chat.id, gif)
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

# Define the /gif3 command handler
@bot.message_handler(commands=['gif3'])
def send_custom_gif3(message):
    if message.from_user.username == '<your telegram username>':
        bot.reply_to(message, "🔴 Wait ....")  
        with open('python_gif\gif3.gif', 'rb') as gif:
            bot.send_document(message.chat.id, gif)
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

# Define the /gif4 command handler
@bot.message_handler(commands=['gif4'])
def send_custom_gif4(message):
    if message.from_user.username == '<your telegram username>':
        bot.reply_to(message, "🔴 Wait ....")
        with open('python_gif\gif4.gif', 'rb') as gif:
            bot.send_document(message.chat.id, gif)
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

# Define the /gif5 command handler
@bot.message_handler(commands=['gif5'])
def send_custom_gif5(message):
    if message.from_user.username == '<your telegram username>':
        bot.reply_to(message, "🔴 Wait ....")
        with open('python_gif\gif5.gif', 'rb') as gif:
            bot.send_document(message.chat.id, gif)
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

# Define the /gif6 command handler
@bot.message_handler(commands=['gif6'])
def send_custom_gif6(message):
    if message.from_user.username == '<your telegram username>':
        bot.reply_to(message, "🔴 Wait ....")
        with open('python_gif\gif6.gif', 'rb') as gif:
            bot.send_document(message.chat.id, gif)
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")
        
# Define the /gif7 command handler
@bot.message_handler(commands=['gif7'])
def send_custom_gif7(message):
    if message.from_user.username == '<your telegram username>':
        bot.reply_to(message, "🔴 Wait ....")
        with open('python_gif\gif7.gif', 'rb') as gif:
            bot.send_document(message.chat.id, gif)
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")
        
# Define the /gif8 command handler
@bot.message_handler(commands=['gif8'])
def send_custom_gif8(message):
    if message.from_user.username == '<your telegram username>':
        bot.reply_to(message, "🔴 Wait ....")
        with open('python_gif\gif8.gif', 'rb') as gif:
            bot.send_document(message.chat.id, gif)
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")
   
# Define the /gif9 command handler     
@bot.message_handler(commands=['gif9'])
def send_custom_gif9(message):
    if message.from_user.username == '<your telegram username>':
        bot.reply_to(message, "🔴 Wait ....")
        with open('python_gif\gif9.gif', 'rb') as gif:
            bot.send_document(message.chat.id, gif)
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

# Define the /gif10 command handler
@bot.message_handler(commands=['gif10'])
def send_custom_gif10(message):
    if message.from_user.username == '<your telegram username>':
        bot.reply_to(message, "🔴 Wait ....")
        with open('python_gif\gif10.gif', 'rb') as gif:
            bot.send_document(message.chat.id, gif)
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")

def take_screenshot():
    time.sleep(2)
    screen_width, screen_height = pyautogui.size()
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    print("Screenshot saved successfully!")

@bot.message_handler(commands=['screenshot'])
def send_screenshot(message):
    if message.from_user.username == '<your telegram username>':
        bot.reply_to(message, "🔴 Taking a screenshot, please wait ....")

        take_screenshot()

        with open('screenshot.png', 'rb') as screenshot:
            bot.send_photo(message.chat.id, screenshot)
        
        print("Screenshot sent successfully!")
    else:
        bot.reply_to(message, "🟥You are not my boss to use this command.👿")
        
ngrok_tunnel = None
 
@bot.message_handler(commands=['ngstart'])
def start_ngrok(message):
    global ngrok_tunnel
    if message.from_user.username == '<your telegram username>':
        local_port = 8080
        try:
            ngrok_tunnel = ngrok.connect(local_port)
            public_url = ngrok_tunnel.public_url
            bot.reply_to(message, "💂‍♀️Ngrok tunnel ✔started successfully.")
            bot_token = '6983779792:AAGF6EHZjYxCFsde0AlXuH4oICYwhlo13ME'
            chat_id = '-1002052206722'
            message = f"Ngrok URL: {public_url}"
            telegram_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
            requests.get(telegram_url)
        except Exception as e:
            print(f"Error: {e}")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")
        
# @bot.message_handler(commands=['ngstart'])
# def start_ngrok(message):
#     global ngrok_tunnel
#     if message.from_user.username == '<your telegram username>':
#         bot.reply_to(message, "Please enter the port number (8080 or 7860):")
#         bot.register_next_step_handler(message, start_ngrok_step2)
#     else:
#         bot.reply_to(message, "You are not authorized to use this command.")

# def start_ngrok_step2(message):
#     global ngrok_tunnel
#     if message.text == '8080' or message.text == '7860':
#         local_port = int(message.text)
#         try:
#             ngrok_tunnel = ngrok.connect(local_port)
#             public_url = ngrok_tunnel.public_url
#             bot.reply_to(message, "💂‍♀️Ngrok tunnel ✔started successfully.")
#             bot_token = 'YOUR_BOT_TOKEN'
#             chat_id = 'YOUR_CHAT_ID'
#             message = f"Ngrok URL: {public_url}"
#             telegram_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
#             requests.get(telegram_url)
#         except Exception as e:
#             print(f"Error: {e}")
#     else:
#         bot.reply_to(message, "Invalid port number. Please enter either 8080 or 7860.")

@bot.message_handler(commands=['ngstop'])
def stop_ngrok(message):
    global ngrok_tunnel
    if message.from_user.username == '<your telegram username>':
        try:
            if ngrok_tunnel:
                ngrok.disconnect(ngrok_tunnel.public_url)
                bot.reply_to(message, "💂‍♀️ngrok web server ❌stopd boss")
                ngrok_tunnel = None  
            else:
                bot.reply_to(message, "Ngrok tunnel is not running.")
        except Exception as e:
            print(f"Error stopping ngrok tunnel: {e}")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

# greeting_users = {}

# @bot.message_handler(commands=['startbom'])
# def start_bom_command(message):
#     bot.reply_to(message, "Hello! Please enter your name:")
#     bot.register_next_step_handler(message, get_user_name)

# def get_user_name(message):
#     user_name = message.text.strip()
#     bot.reply_to(message, f"Hello {user_name}! I will keep saying hello until you send /done.")
#     greeting_users[message.chat.id] = True
#     continuously_say_hello(message.chat.id)

# def continuously_say_hello(chat_id):
#     while greeting_users.get(chat_id, False):
#         bot.send_message(chat_id, "Hello! Type /done when you want to stop.")
#         time.sleep(1)  # You can adjust the sleep duration

# @bot.message_handler(commands=['done'])
# def done_command(message):
#     chat_id = message.chat.id
#     if greeting_users.get(chat_id, False):
#         greeting_users[chat_id] = False
#         bot.reply_to(message, "Okay! I will stop saying hello.")
#     else:
#         bot.reply_to(message, "I'm not currently greeting you.")


# Define the /datetime command handler
@bot.message_handler(commands=['datetime'])
def show_date_time(message):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    bot.reply_to(message, f"The current date and time is: \n🟥 {formatted_datetime} 🟥")

@bot.message_handler(func=lambda message: any(keyword in message.text.lower() for keyword in ['tnk', 'thanks', "thank"]))
def handle_thanks(message):
    bot.reply_to(message, "👍Your welcome bro 💂‍♀️❤")

@bot.message_handler(func=lambda message: any(keyword in message.text.lower() for keyword in ['hi', 'hello', "hey", "what's up"]))
def handle_thanks(message):
    abbas_text_list = ["🤖What's up my nigger ? 🖐🏿💪🏿", "hey dood 👦🏿😎", "hey homie 🖐🤜"]
    bot.reply_to(message, f"{random.choice(abbas_text_list)}")

@bot.message_handler(func=lambda message: True)
def handle_username_command(message):
    global user_id_counter
    
    if message.reply_to_message and message.reply_to_message.text == "Please type your name:":
        username = message.text.strip()

        user_id = user_id_counter
        user_id_counter += 1
        usernames[user_id] = {'user-id': user_id, 'user-name': username}
        save_usernames_to_json()
        bot.reply_to(message, f"Hello, {username}!")

    else:
        pass

def save_usernames_to_json():
    with open('usernames.json', 'w') as json_file:
        json.dump(usernames, json_file, indent=4)

# Start the bot :)
bot.infinity_polling()









#  █████╗ ███╗   ███╗██╗██████╗  █████╗ ██████╗ ██████╗  █████╗ ███████╗    ██████╗  ██████╗ ██╗   ██╗██╗███╗   ██╗████████╗ █████╗ ███╗   ██╗
# ██╔══██╗████╗ ████║██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔═══██╗██║   ██║██║████╗  ██║╚══██╔══╝██╔══██╗████╗  ██║
# ███████║██╔████╔██║██║██████╔╝███████║██████╔╝██████╔╝███████║███████╗    ██████╔╝██║   ██║██║   ██║██║██╔██╗ ██║   ██║   ███████║██╔██╗ ██║
# ██╔══██║██║╚██╔╝██║██║██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══██║╚════██║    ██╔══██╗██║   ██║██║   ██║██║██║╚██╗██║   ██║   ██╔══██║██║╚██╗██║
# ██║  ██║██║ ╚═╝ ██║██║██║  ██║██║  ██║██████╔╝██████╔╝██║  ██║███████║    ██║  ██║╚██████╔╝╚██████╔╝██║██║ ╚████║   ██║   ██║  ██║██║ ╚████║
# ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
