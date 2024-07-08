import sys
import os


sus_key_received = False 


'''
Detect if the user pressed an arrow key and return it if this happend.
@param "key" : the pressed key
'''
def detect_arrow_key(key):
    global sus_key_received
    if ord(key) == 224 and not sus_key_received:
        sus_key_received = True
        return None
    elif ord(key) == 72 and sus_key_received:
        sus_key_received = False
        return "ARROW UP"
    elif ord(key) == 77 and sus_key_received:
        sus_key_received = False
        return "ARROW RIGHT"
    elif ord(key) == 80 and sus_key_received:
        sus_key_received = False
        return "ARROW DOWN"
    elif ord(key) == 75 and sus_key_received:
        sus_key_received = False
        return "ARROW LEFT"
    return ""


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
            arrow_key = detect_arrow_key(key)
            if key == b'\t' and arrow_key == None:      # Up
                return "CTRL+i"
            elif key == b'\x0c' and arrow_key == None:  # Right
                return "CTRL+l"
            elif key == b'\x0b' and arrow_key == None:  # Down
                return "CTRL+k"
            elif key == b'\n' and arrow_key == None:    # Left
                return "CTRL+j"
            elif key == b'\x0f' and arrow_key == None:  # Fast right
                return "CTRL+o"
            elif key == b'\x15' and arrow_key == None:  # Fast left
                return "CTRL+u"
            elif key == b'\x17' and arrow_key == None:  # Close
                return "CTRL+w"
            elif key == b"\x08" and arrow_key == None:  # Backspace/Delete key
                return "DELETE"
            elif key == b"\xe0" and arrow_key == None:
                return "CANCEL"
            elif arrow_key != None:
                return arrow_key
            elif arrow_key == "":
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
