import re
import socket
import json
import threading
from emoji import demojize
from TTSHandler import TTSHandler

DEFAULT_TWITCH_FILE = 'twitch_config.json'


def decode(message):
    message = demojize(message).replace('\r', '')
    username, channel, message = re.search(r':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*?) :(.*)', message).groups()
    # remove web links
    message = re.sub(r'http(s?)://\S+|\S+\.com/\S+', 'web link', message)
    return username, message


class TwitchReader(threading.Thread):
    def __init__(self, name='TwitchReader'):
        threading.Thread.__init__(self)
        self.name = name

        # keep sensitive information stored in a separate config file
        self._config = {
            'server': 'irc.chat.twitch.tv',
            'port': 6667,
            'nickname': 'bot',
            'token': 'oauth:TOKENHERE',
            'channel': '#channelname'
        }
        self.load_config()

        self.debug_output = False
        self.handler = None
        self.running = False

    def load_config(self, filename=DEFAULT_TWITCH_FILE):
        try:
            with open(filename, 'r') as f:
                self._config.update(json.load(f))
        except IOError:
            pass

    def save_config(self, filename=DEFAULT_TWITCH_FILE):
        with open(filename, 'w+') as f:
            json.dump(self._config, f)

    def stop(self):
        self.running = False

    def run(self):
        print('Connecting to Twitch')
        sock = socket.socket()
        sock.connect((self._config['server'], self._config['port']))
        sock.send(f'PASS {self._config["token"]}\n'.encode('utf-8'))
        sock.send(f'NICK {self._config["nickname"]}\n'.encode('utf-8'))
        sock.send(f'JOIN {self._config["channel"]}\n'.encode('utf-8'))

        print('Entering Chat loop')
        self.running = True
        while self.running:
            resp = sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                sock.send("PONG :tmi.twitch.tv2 3\n".encode('utf-8'))
            elif len(resp) > 0 and 'PRIVMSG' in resp:
                if self.handler is not None:
                    username, message = decode(resp)
                    self.handler.receive(username, message)
                    # sock.send(f'PRIVMSG {self._config["channel"]} :received message\n'.encode('utf-8'))
            if self.debug_output:
                print(resp)
        print('Closing socket')
        sock.close()


if __name__ == '__main__':
    reader = TwitchReader()
    reader.handler = TTSHandler()
    reader.debug_output = True
    reader.run()
