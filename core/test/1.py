import threading
import time


def test():
    print(1)
    time.sleep(3)
    print(2)


def push_button():
    t = threading.Thread(target=test)
    t.start()
    print(333333333)


push_button()
print(4444444444)
