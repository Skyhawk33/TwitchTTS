# Twitch TTS

This is a custom text to speech program using the **pyttsx3** library.

Gives new users a random voice selected from the ones installed, and allows them to change their voice using the `!voice` command. 

## Installation

1. Install the latest version of [Python](https://www.python.org/downloads/).
2. Download the [contents of this repository](https://github.com/Skyhawk33/TwitchTTS/archive/refs/heads/main.zip) and unzip them into a folder.
3. Copy `twitch_config_TEMPLATE.json` and rename it to `twitch_config.json`.
4. Open `twitch_config.json` with Notepad and do the following:
	1. Generate an OAuth token for your channel using [this tool](https://twitchapps.com/tmi/) and replace `TOKENHERE` with the generate token.
	2. Replace `#channelname` with the name of your channel (keeping the `#`).
	3. Save your changes.
5. Create a new file called `users.json` which just contains `{}`.
6. In the folder you unzipped the contents of this repo into, open the command line by clicking the address bar of the folder and typing `cmd` and then hitting enter.
7. Run the following commands
	1. `pip install pyttsx3`
	2. `pip install emoji`
8. The TTS is now ready to be used, and can be ran by double clicking `Main.py`.

## Using Alternate Voices

Alternate voices can be used by a user, but the voice package must first be installed on your machine before running `Main.py`.

A user can switch voices by using typing the command `!voice [Speaker] [Rate]`.

The `[Speaker]` value can be either a `code` or a `name` from the table below.

|Language|Code|Name|
|---|---|---|
|English (US) (Male)|US|David|
|English (US) (Female)|US|Zira|
|English (GB)|GB|Hazel|
|German|DE|Hedda|
|Spanish (Spain)|ES|Helena|
|Spanish (Mexico)|MX|Sabina|
|French|FR|Hortense|
|Italian|IT|Elsa|
|Japanese|JP|Haruka|
|Korean|KR|Heami|
|Polish|PL|Paulina|
|Portrugese|BR|Maria|
|Russian|RU|Irina|
|Chinese (China)|CN|Huihui|
|Chinese (Hong Kong)|HK|Tracy|
|Chinese (Taiwan)|TW|Hanhan|

In cases where the `code` is the same for different speakers, the speaker name must be specified instead.

The `rate` is a number (the default is 200).
