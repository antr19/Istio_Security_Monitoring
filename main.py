import time
import os
import telebot

from istio_parser import istio_checking, stay_alive
from github_security import envoy_checking

token = os.environ['TG_TOKEN']
channel = os.environ['TG_CHANNEL']
admin = os.environ['TG_ADMIN']
bot = telebot.TeleBot(token)

start_data = time.asctime(time.localtime())

bot.send_message(admin, "I'm starting!\n" + start_data)

attempt = 0
while True:
    tt = time.time()
    while time.time() - tt < 15*60:
        stay_alive()
        time.sleep(30)

    if attempt == 32:
        bot.send_message(admin, "I alive!!!\n" + start_data)
        attempt = 0

    istio_report = istio_checking()
    if istio_report:
        bot.send_message(channel, istio_report, parse_mode='HTML')
    envoy_report = envoy_checking()
    if envoy_report:
        bot.send_message(channel, envoy_report, parse_mode="HTML")
    attempt += 1