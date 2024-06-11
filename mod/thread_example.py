import threading
import time
import sys

# Event object for safe thread termination
stop_event = threading.Event()

def logic():
    while not stop_event.is_set():
        print("Funzione in esecuzione in un thread")
        time.sleep(2)

if sys.platform == 'win32':
    import msvcrt

    def get_key():
        return msvcrt.getch().decode('utf-8')

else:
    import tty
    import termios
    import sys

    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key

def read_input():
    while True:
        user_input = get_key()
        print(user_input)

        if user_input == "e":
            stop_event.set()  # Signal threads to stop
            break

def main():
    main_thread = threading.Thread(target=logic)
    input_thread = threading.Thread(target=read_input)

    main_thread.start()
    input_thread.start()

    # Wait for both threads to finish before exiting
    main_thread.join()
    input_thread.join()

main()
