import threading
import time

# Event object for safe thread termination
stop_event = threading.Event()


def logic():
    while not stop_event.is_set():
        print("Funzione in esecuzione in un thread")
        time.sleep(2)


def read_input():
    while True:
        user_input = input()
        print(user_input)

        if user_input == "end":
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
