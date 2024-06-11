import threading
import time
import sys
import os

# Event object for safe thread termination
stop_event = threading.Event()


if sys.platform == "win32":
    import msvcrt

    def get_key():
        while True:
            key = msvcrt.getch()
            if key == b"\x0D":  # Ctrl+M (Enter key)
                return "CTRL+M"
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
            if ord(key) == 13:  # Ctrl+M (Enter key)
                return "CTRL+M"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key


def logic():
    while not stop_event.is_set():
        print("Funzione in esecuzione in un thread")
        time.sleep(0.1)


def read_input():
    while True:
        user_input = get_key()
        print(user_input)

        if user_input == "CTRL+M":
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
