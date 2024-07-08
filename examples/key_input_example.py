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
Print useful informations about the pressed key
'''
def key_debugger(key):
    print(type(key), end=" ~ ")
    print(ord(key), end=" ~ ")
    print(key, end=" ~ ")
    print(chr(ord(key)))


'''
Return the respective key/combination pressed by the user@
@param "key" : native variable containing the pressed key
@param "arrow_key" : container for the arrow key
'''
def key_identifier(key, arrow_key):
	if ord(key) == 9 and arrow_key == None:      # Up
		return "CTRL+i"
	elif ord(key) == 12 and arrow_key == None:  # Right
		return "CTRL+l"
	elif ord(key) == 11 and arrow_key == None:  # Down
		return "CTRL+k"
	elif ord(key) == 10 and arrow_key == None:    # Left
		return "CTRL+j"
	elif ord(key) == 15 and arrow_key == None:  # Fast right
		return "CTRL+o"
	elif ord(key) == 21 and arrow_key == None:  # Fast left
		return "CTRL+u"
	elif ord(key) == 23 and arrow_key == None:  # Close
		return "CTRL+w"
	elif ord(key) == 127 and arrow_key == None:  # Backspace/Delete key
		return "DELETE"
	elif ord(key) == 126 and arrow_key == None:
		return "CANCEL"
	elif arrow_key != None:
		return arrow_key
	elif arrow_key == "":
        return key.decode("utf-8")

'''
Detect special keys pressed by the user
'''
if sys.platform == "win32":
    import msvcrt

    def get_key():
        while True:
            key = msvcrt.getch()
            key_debugger(key)
            arrow_key = detect_arrow_key(key)
            return key_identifer(key, arrow_key)
else:
    import tty
    import termios

    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
            key_debugger(key)
            arrow_key = detect_arrow_key(key)
            return key_identifer(key, arrow_key)
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
