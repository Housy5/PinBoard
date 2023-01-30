from models import Pin
from models import PinBoard
from models import NoSuchIDException

import os
import pickle

board = None
push_file_name = "pins.pin"
settings_file_name = "settings.pin"
auto_push = True
running = True

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_settings():
    file = open(settings_file_name, "w")
    file.write('1' if auto_push else '0')
    file.close()

def load_settings():
    global auto_push
    if not os.path.isfile(settings_file_name):
        return
    file = open(settings_file_name, "r")
    auto_push = True if file.read() == '1' else False
    file.close()

def push_to_file():
    file = open(push_file_name, "wb")
    pickle.dump(board, file)
    file.close()
    print("Push successful.")

def load_from_file():
    global board
    
    if not os.path.isfile(push_file_name):
        board = PinBoard()
        return
    
    file = open(push_file_name, 'rb')
    board = pickle.load(file)
    file.close()
    board.scan_pins()

def pin(msg: str):
    new_pin = Pin(msg)
    if not board.add_pin(new_pin):
        print('Failed to add a new pin.')
        return
    print("Successfully added a new pin!")

def unpin(id: str):
    try:
        pin: Pin = board.find_pin_by_id(id)
        board.remove_pin(pin)
    except NoSuchIDException as e:
        print(e)
    
def print_pins():
    pins: list[Pin] = board.board
    for x in pins:
        print(f"ID: {x.get_id()}\tMessage: {x.get_message()}.")

def print_help():
    print("All Commands: ")
    print("\thelp - Shows this text.")
    print("\tcls  - Clears the console.")
    print("\tpin [text] - Adds a new pin.")
    print("\tunpin [ID] - Removes an existing pin.")
    print("\texit - Exits the program.")
    print("\tauto_push - Toggles automatic saving.")
    print("\tpush - Saves the current state of the program.")

def main():
    global running
    global auto_push
    
    print(Pin._used_ids)
    
    user_input: str = input(' >> ').casefold()
    if user_input.startswith('pin '):
        pin(user_input[4:])
        if (auto_push):
            push_to_file()
    elif user_input == 'pins':
        print_pins()
    elif user_input.startswith('unpin '):
        unpin(user_input[6:])
        if (auto_push):
            push_to_file()
    elif user_input == 'cls':
        clear_console()
    elif user_input == 'exit':
        running = False
    elif user_input == 'push':
        push_to_file()
    elif user_input == 'auto_push':
        auto_push = not auto_push
        msg = "Auto push enabled" if auto_push else "Auto push disabled."
        print(msg)
        save_settings()
    elif user_input == 'help':
        print_help()

def static_init():
    load_from_file()

if __name__ ==  '__main__':
    static_init()
    load_settings()
    while (running):
        main()