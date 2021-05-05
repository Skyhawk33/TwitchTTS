import pyttsx3
import json
import threading
import random

DEFAULT_USER_FILE = 'users.json'
BANNED_USERS = {'nightbot'}


class TTSHandler(threading.Thread):
    def __init__(self, name='TTSHandler'):
        threading.Thread.__init__(self)
        self.name = name
        self.users = {}
        self.engine = None
        self.voices = []
        self.load_users()

        self.message_queue = []
        self.message_condition = threading.Condition()
        self.running = False

    def load_users(self, filename=DEFAULT_USER_FILE):
        with open(filename, 'r') as f:
            file_users = json.load(f)
            self.users.update(file_users)

    def save_users(self, filename=DEFAULT_USER_FILE):
        with open(filename, 'w') as f:
            json.dump(self.users, f)

    def receive(self, username, message):
        self.message_condition.acquire()
        self.message_queue.append((username, message))
        self.message_condition.notify()
        self.message_condition.release()

    def stop(self):
        self.message_condition.acquire()
        self.running = False
        self.message_condition.notify()
        self.message_condition.release()

    def change_voice(self, username, message):
        tokens = message.split(' ')
        if tokens[0] != '!voice':
            return False

        voice_name = tokens[1].upper()

        voice = self.users[username][0]
        for i, v in enumerate(self.voices):
            id_name = str(v.id).rsplit('\\', 1)[1].strip('1234567890._').upper()
            # handle 2 letter codes separately, so that we dont just match the first name that contains those letters
            if len(voice_name) == 2 and f'{voice_name}-' in id_name or f'{voice_name}_' in id_name:
                voice = i
                break
            elif voice_name in id_name:
                voice = i
                break

        try:
            rate = int(tokens[-1])
        except ValueError:
            rate = self.users[username][1]

        self.users[username] = (voice, rate)
        return True

    def run(self):
        print('Handler Starting!')
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')

        self.running = True
        has_messages = False
        while self.running:
            self.message_condition.acquire()
            while not self.message_queue and self.running:
                self.message_condition.wait()

            for username, message in self.message_queue:
                if username in BANNED_USERS:
                    continue
                if username not in self.users:
                    self.users[username] = (random.randrange(len(self.voices)), random.randint(180, 220))

                if message.startswith('!voice '):
                    if self.change_voice(username, message):
                        self.engine.setProperty('voice', self.voices[self.users[username][0]].id)
                        self.engine.setProperty('rate', self.users[username][1])
                        self.engine.say(f'{username} has changed voices')
                else:
                    try:
                        self.engine.setProperty('voice', self.voices[self.users[username][0]].id)
                    except IndexError:
                        self.engine.setProperty('voice', self.voices[0].id)
                    self.engine.setProperty('rate', self.users[username][1])
                    self.engine.say(message)
                has_messages = True
            self.message_queue.clear()

            self.message_condition.release()
            # release the lock so that other messages can be queued while current ones are read
            if has_messages:
                self.engine.runAndWait()
                has_messages = False
        print('Handler stopping')


def test():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for i, v in enumerate(voices):
        print(v.id, f'\t[{i}]')
        engine.setProperty('voice', v.id)
        engine.say('this is a test message')
    engine.runAndWait()


if __name__ == '__main__':
    test()
