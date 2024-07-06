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
            if key == b'\t':      # Up
                return "CTRL+I"
            elif key == b'\x0c':  # Right
                return "CTRL+L"
            elif key == b'\r':    # Down
                return "CTRL+M"
            elif key == b'\n':    # Left
                return "CTRL+J"
            elif key == b'\x0f':  # Fast right
                return "CTRL+O"
            elif key == b'\x15':  # Fast left
                return "CTRL+U"
            elif key == b'\x17':  # Close
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
            print(ord(key))
            if ord(key) == 9:     # Up
                return "CTRL+I"
            elif ord(key) == 12:  # Right
                return "CTRL+L"
            elif ord(key) == 13:  # Down
                return "CTRL+M"
            elif ord(key) == 10:  # Left
                return "CTRL+J"
            elif ord(key) == 23:  # Close
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
