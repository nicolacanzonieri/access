'''
PYTHONISTA THREAD EXAMPLE
'''

import threading
import time
import ui # type: ignore

# Event object for safe thread termination
stop_event = threading.Event()

def logic():
    while not stop_event.is_set():
        print("Funzione in esecuzione in un thread")
        time.sleep(2)

def read_input(textfield):
    while True:
        user_input = textfield.text
        if user_input:
            print(user_input)
            textfield.text = ''  # Clear the text field

            if user_input == "e":
                stop_event.set()  # Signal threads to stop
                break

def main():
    # Create UI elements
    view = ui.View()
    textfield = ui.TextField(frame=(10, 10, 200, 40))
    view.add_subview(textfield)
    
    def textfield_action(sender):
        user_input = sender.text
        if user_input:
            print(user_input)
            sender.text = ''  # Clear the text field

            if user_input == "e":
                stop_event.set()  # Signal threads to stop

    textfield.action = textfield_action

    # Start the threads
    main_thread = threading.Thread(target=logic)
    input_thread = threading.Thread(target=read_input, args=(textfield,))

    main_thread.start()
    input_thread.start()

    # Present the UI
    view.present('sheet')

    # Wait for both threads to finish before exiting
    main_thread.join()
    input_thread.join()

main()
