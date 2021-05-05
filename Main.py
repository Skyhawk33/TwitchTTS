from TTSHandler import TTSHandler
from TwitchReader import TwitchReader

if __name__ == '__main__':
    reader = TwitchReader()
    handler = TTSHandler()
    reader.handler = handler

    handler.start()
    reader.start()

    input('Main: ENTER ANYTHING TO HALT\r\n')
    print('Main: closing')
    handler.save_users()

    reader.stop()
    handler.stop()

    reader.join()
    handler.join()
