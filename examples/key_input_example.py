import sys
import os

'''
Detect special keys pressed by the user
'''
if sys.platform == "win32":
    import msvcrt

    def get_key():
        while True:
            key = msvcrt.getch()
            print(key)
            if key == b"\x0D":  # Ctrl+M (Enter key)
                return "CTRL+M"
            elif key == b"\x11":  # Ctrl+Q
                return "CTRL+Q"
            elif key == b'\x17':  # Ctrl+W
                return "CTRL+W"
            elif key == b"\x08":  # Backspace/Delete key
                return "DELETE"
            elif key == b"\xe0":
                return "CANCEL"
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
            if ord(key) == 13:
                return "CTRL+M"
            elif ord(key) == 17:
                return "CTRL+Q"
            elif ord(key) == 23:
                return "CTRL+W"
            elif ord(key) == 127:
                return "DELETE"
            elif ord(key) == 126:
                return "CANCEL"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key

def start_example():
    while True:
        # USER KEY GETTER
        try:
            user_input = get_key()
        except:
            user_input = ""
        
        print(user_input)
        
        # USER INPUT HANDLER
        if user_input == "CTRL+W":
            break
        elif user_input == "CTRL+Q":
            break
