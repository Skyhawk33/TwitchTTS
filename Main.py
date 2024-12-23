import time

from TTSHandler import TTSHandler
from TwitchReader import TwitchReader

if __name__ == '__main__':
    reader = TwitchReader()
    handler = TTSHandler()
    reader.handler = handler

    handler.start()
    reader.start()

    print('Main: Running. Press Ctrl+C to halt.')
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print('Main: Interrupted, stopping.')

    print('Saving user changes...')
    handler.save_users()

    print('Stopping threads...')
    reader.stop()
    handler.stop()

    reader.join()
    handler.join()
