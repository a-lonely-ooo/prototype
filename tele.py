import requests
import time
import os
import sys

# ANSI Color Codes
class Color:
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# Typing effect printer
def typing_print(text, color=Color.WHITE, speed=0.03):
    colored_text = color + text + Color.RESET
    for char in colored_text:
        print(char, end='', flush=True)
        time.sleep(speed)
    print()

# Custom rotating logo animation (appears after DOSTS)
def show_logo_animation():
    frames = [
        r"""
          _____
         /     \
        | O   O |
         \  ▽  /
          ─────
        LOADING...
        """,
        r"""
          _____
         /     \
        | O   O |
         \  ▽  /
          ─────
        LOADING...
        """,
        r"""
          _____
         /     \
        | O   O |
         \  ▽  /
          ─────
        LOADING...
        """
    ]
    
    # Add rotation variants
    rotated_frames = []
    for frame in frames:
        rotated_frames.append(frame.replace('O', '◐').replace('△', '◑'))
        rotated_frames.append(frame.replace('O', '◓').replace('△', '◒'))
        rotated_frames.append(frame.replace('O', '◑').replace('△', '◐'))
        rotated_frames.append(frame.replace('O', '◒').replace('△', '◓'))
    
    end_time = time.time() + 2  # 2 seconds duration
    while time.time() < end_time:
        for frame in rotated_frames:
            clear()
            print(Color.CYAN + frame + Color.RESET)
            time.sleep(0.1)

# Fade-in animation for ASCII art
def fade_in_ascii_art():
    ascii_art = [
        "░█─░█ █── ▀▀█▀▀ ─▀─ █▀▄▀█ █▀▀█ ▀▀█▀▀ █▀▀ 　 ▀█▀ █▀▀▄ █▀▀ ▀▀█▀▀ █▀▀█ 　 █── █▀▀█ █▀▀█ █─█ █──█ █▀▀█",
        "░█─░█ █── ──█── ▀█▀ █─▀─█ █▄▄█ ──█── █▀▀ 　 ░█─ █──█ ▀▀█ ──█── █▄▄█ 　 █── █──█ █──█ █▀▄ █──█ █──█",
        "─▀▄▄▀ ▀▀▀ ──▀── ▀▀▀ ▀───▀ ▀──▀ ──▀── ▀▀▀ 　 ▄█▄ ▀──▀ ▀▀▀ ──▀── ▀──▀ 　 ▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀─▀ ─▀▀▀ █▀▀▀",
        "                          Github: @a-lonely-ooo",
        "                          insta: @a_lonely_ooo",
        "                          telegram: @a_lonely_ooo",
        "                          twitter: @a_lonely_ooo",
        "                          discord: @a_lonely_ooo",
        "Yah I am addicted to this username😅"
    ]
    
    max_length = max(len(line) for line in ascii_art)
    steps = 15
    delay = 0.03
    
    for i in range(steps + 1):
        clear()
        ratio = i / steps
        for line in ascii_art:
            visible_chars = int(len(line) * ratio)
            faded_line = Color.MAGENTA + line[:visible_chars] + Color.RESET
            print(faded_line)
        time.sleep(delay)
    print()

# Original animations
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_lookup():
    for i in range(3):
        clear()
        print("LOOKUP...")
        time.sleep(0.5)
        clear()
        print("LOOKUP")
        time.sleep(0.5)

def display_dosts():
    for i in range(3):
        clear()
        print("DOSTS...")
        time.sleep(0.5)
        clear()
        print("DOSTS")
        time.sleep(0.5)
    show_logo_animation()  # Added rotating logo after DOSTS

def main():
    # ASCII art with fade-in animation
    fade_in_ascii_art()
    
    typing_print("Credit must🫶: @a_lonely_ooo", Color.MAGENTA, 0.03)
    
    # Original input prompt
    typing_print(Color.YELLOW + Color.BOLD + "Enter the id without @ symbol: " + Color.RESET, speed=0)
    username = input()
    
    # API request
    params = {'username': username}
    data = requests.get("https://trendhero.io/api/get_er_reports", params=params, headers={
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'sec-ch-ua': "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\"",
        'sec-ch-ua-mobile': "?1",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://trendhero.io/instagram-follower-count/",
        'accept-language': "en-US,en;q=0.9",
    }).json()
    
    user_info = data['preview']['user_info']
    post_info = data['preview']['posts'][0] if data['preview']['posts'] else {}
    
    # Display account info
    typing_print("### Account Information ###", Color.GREEN, 0.02)
    typing_print(f"ID: {user_info['id']}", Color.CYAN)
    typing_print(f"Username: {user_info['username']}", Color.CYAN)
    typing_print(f"Full Name: {user_info['full_name']}", Color.CYAN)
    typing_print(f"Profile Picture: {user_info['profile_pic_url']}", Color.CYAN)
    typing_print(f"Followers: {user_info['follower_count']}", Color.CYAN)
    typing_print(f"Following: {user_info['following_count']}", Color.CYAN)
    typing_print(f"Posts: {user_info['media_count']}", Color.CYAN)
    typing_print(f"Verified: {'✅' if user_info['is_verified'] else '❌'}", 
                Color.GREEN if user_info['is_verified'] else Color.RED)
    typing_print(f"Private Account: {'✅' if user_info['is_private'] else '❌'}", 
                Color.GREEN if not user_info['is_private'] else Color.RED)
    typing_print(f"Business Account: {'✅' if user_info['is_business_account'] else '❌'}", 
                Color.GREEN if user_info['is_business_account'] else Color.YELLOW)
    typing_print(f"Bio: {user_info['biography'] or 'Not available'}", Color.CYAN)
    
    if post_info:
        typing_print("\n### Last Post ###", Color.GREEN, 0.02)
        typing_print(f"Post ID: {post_info['pk']}", Color.CYAN)
        typing_print(f"Shortcode: {post_info['shortcode']}", Color.CYAN)
        typing_print(f"Likes: {post_info['likes']}", Color.CYAN)
        typing_print(f"Comments: {post_info['comments']}", Color.CYAN)
        typing_print(f"Views: {post_info['views']}", Color.CYAN)
    else:
        typing_print("\nNo posts available", Color.YELLOW)
    
    typing_print("\nCredit must🫶: @a_lonely_ooo", Color.MAGENTA)

if __name__ == "__main__":
    display_lookup()
    display_dosts()
    main()