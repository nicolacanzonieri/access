import sys
import os


banned_keys = []
def detect_banned_key(key):
    global banned_keys
    if ord(key) == 224 and len(banned_keys) == 0:
        banned_keys.append(ord(key))
        print("CHECK 1")
        return None
    elif (ord(key) == 72 or ord(key) == 77 or ord(key) == 80 or ord(key) == 75) and len(banned_keys) == 1:
        print("CHECK 2 - POSITIVE")
        banned_keys = []
        return True
    else:
        print("CHECK 2 - NEGATIVE")
        banned_keys = []
        return False


'''
Detect special keys pressed by the user
'''
if sys.platform == "win32":
    import msvcrt

    def get_key():
        while True:
            key = msvcrt.getch()
            print(type(key), end=" ~ ")
            print(ord(key), end=" ~ ")
            print(key, end=" ~ ")
            print(chr(ord(key)))
            key_check = detect_banned_key(key)
            if key == b'\t' and key_check == False:      # Up
                return "CTRL+i"
            elif key == b'\x0c' and key_check == False:  # Right
                return "CTRL+l"
            elif key == b'\x0b' and key_check == False:  # Down
                return "CTRL+k"
            elif key == b'\n' and key_check == False:    # Left
                return "CTRL+j"
            elif key == b'\x0f' and key_check == False:  # Fast right
                return "CTRL+o"
            elif key == b'\x15' and key_check == False:  # Fast left
                return "CTRL+u"
            elif key == b'\x17' and key_check == False:  # Close
                return "CTRL+w"
            elif key == b"\x08" and key_check == False:  # Backspace/Delete key
                return "DELETE"
            elif key == b"\xe0" and key_check == False:
                return "CANCEL"
            elif key_check == False:
                return key.decode("utf-8")

else:
    import tty
    import termios

    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
            print(ord(key))
            if ord(key) == 9:     # Up
                return "CTRL+i"
            elif ord(key) == 12:  # Right
                return "CTRL+l"
            elif ord(key) == 11:  # Down
                return "CTRL+k"
            elif ord(key) == 10:  # Left
                return "CTRL+j"
            elif ord(key) == 15:  # Fast right
                return "CTRL+o"
            elif ord(key) == 21:  # Fast left
                return "CTRL+u"
            elif ord(key) == 23:  # Close
                return "CTRL+w"
            elif ord(key) == 127:
                return "DELETE"
            elif ord(key) == 126:
                return "CANCEL"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key

def start_key_input_example():
    while True:
        # USER KEY GETTER
        try:
            user_input = get_key()
        except:
            user_input = ""
        
        print(user_input)
        
        # USER INPUT HANDLER
        if user_input == "CTRL+w":
            break
