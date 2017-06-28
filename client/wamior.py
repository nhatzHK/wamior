import sys
import discord
import logging
import asyncio
import json

PATH = dict ()
if (len (sys.argv) > 1):
    try:
        with open (sys.argv [1]) as path_file:
            PATH = json.load (path_file)
    except:
        print ('Unable to open file {}'.format (sys.argv [1]))
        exit (2)
else:
    print ("Usage: python wamior.py /path/to/path.json")
    exit (1)

sys.path.insert (0, PATH['lib'])
import client_helpers as CLIENT
import parser_helpers as PARSER

CONFIG = dict ()
CONFIG = CLIENT.loadJson (PATH['config'])

logging.basicConfig (level = logging.INFO)

Wame = discord.Client ()
wgame = discord.Game (name = CONFIG['game'])

@Wame.event
async def on_ready ():
    await Wame.change_presence (game = wgame)
    bug_channel = Wame.get_channel (CONFIG['report_channel'])
    CLIENT.greet (Wame, channel = bug_channel)

@Wame.event
async def on_message (message):
    if not message.content.startswith (CONFIG['prefix']):
        pass
    else:
        args = await CLIENT.parse_args (message.content)
        logging.info ('\nFull mess: {}\nCommand :{}\nArgs   : {}'\
                .format (message.content, args[0], args[1:]))

        command = args [0]
        if len (args) == 0:
            pass
        elif command == "wiki":
            tmp = await Wame.send_message (message.channel, 
                    'Searching ArchWiki...')
            result = PARSER.get_section (' '.join(args[1:]), 0)
            if result['status'] == 0:
                clean = PARSER.extract_text (result['html'])
                await Wame.edit_message (tmp, clean['text'])
            else:
                await Wame.edit_message (tmp, 'Not found.')
        elif command == "repo":
            tmp = await Wame.send_message (message.channel,
                    'Searching Official repos...')
            result = PARSER.search_ss (' '.join(args[1:]))
            await Wame.edit_message(tmp, 'Name: {}\nDescription: {}\n \
                    Repo: {}\nURL: {}\n'.format \
                    (result['name'], result['description'], result['repo'], \
                    result['url']))
        elif command == "aur":
            tmp = await Wame.send_message (message.channel,
                    'Searching AUR...')
        elif command == "pkg":
            tmp = await Wame.send_message (message.channel,
                    'Searching Official repos and AUR...')
        elif command == "help":
            tmp = await Wame.send_message (message.channel,
                    'Weew a looser asking for help...')
        elif command == "report":
            tmp = await Wame.send_message (message.channel,
                    'I\'m a perfect bot. Go away!')

Wame.run (CONFIG['token'])
