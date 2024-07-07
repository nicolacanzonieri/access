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
            print(ord(key))
            if key == b'\t':      # Up
                return "CTRL+i"
            elif key == b'\x0c':  # Right
                return "CTRL+l"
            elif key == b'\x0b':  # Down
                return "CTRL+k"
            elif key == b'\n':    # Left
                return "CTRL+j"
            elif key == b'\x0f':  # Fast right
                return "CTRL+o"
            elif key == b'\x15':  # Fast left
                return "CTRL+u"
            elif key == b'\x17':  # Close
                return "CTRL+w"
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
