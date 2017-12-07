#!/usr/bin/env python

import time
import telegram
import os.path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PATH = '' # Ruta de la carpeta que se desea monitorizar.
USER_ID =  # ID del usuario a quien enviar las notificaciones.
TOKEN = '' # Token del Bot de Telegram.

class SendMessageTg():
    def send_text(self, event, path):

        bot = telegram.Bot(TOKEN)
        msg = "____________________\nEvent: %s\nFile: %s\n____________________" % (event,path)
        bot.send_message(chat_id=USER_ID, text=msg)
        print 'send message'

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        smtg = SendMessageTg()
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            smtg.send_text('created', event.src_path)
        elif event.event_type == 'modified':
            smtg.send_text('modified', event.src_path)
        elif event.event_type == 'moved':
            smtg.send_text('moved', event.src_path)
        elif event.event_type == 'deleted':
            smtg.send_text('deleted', event.src_path)

def start(bot, update):
    update.message.reply_text('Hi!')

def viewFile(bot,update,args):
    for arg in args:
        if os.path.isfile(arg):
            try:
                bot.send_document(chat_id=USER_ID, document=open(arg, 'rb'))
            except:
                print "error to send file"
        else:
            bot.send_message(chat_id=USER_ID, text= 'not is file '+arg)


def help(bot, update):
    msg = """
       /help
       /tail
       /getFile
       /delFile
       /touchFile
       /mvFile
       /cpFile
    """
    update.message.reply_text(msg)

def echo(bot, update):
    update.message.reply_text(update.message.text)

def error(bot, update, error):
    print 'Update "%s" caused error "%s"' % (update, error)

def main():
    # watchdog
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, PATH, recursive=True)
    observer.start()
    # end watchdog
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CommandHandler("getFile", viewFile, pass_args=True))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
