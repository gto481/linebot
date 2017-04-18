# -*- coding: utf-8 -*-
# from chatterbot import ChatBot
# import train_bot
# import location_bot
import test_wit
from pprint import pprint
import dateparser

# bot = ChatBot('LineBot',
#     storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
#     logic_adapters=[
#         'chatterbot.logic.BestMatch',
#         'chatterbot.logic.MathematicalEvaluation',
#         'chatterbot.logic.TimeLogicAdapter'
#     ],
#     filters=[
#         'chatterbot.filters.RepetitiveResponseFilter'
#     ],
#     input_adapter="chatterbot.input.VariableInputTypeAdapter",
#     output_adapter="chatterbot.output.OutputAdapter",
#     output_format="text",
#     database='heroku_h80dpwn6',
#     database_uri='mongodb://bot:bot123@ds027425.mlab.com:27425/heroku_h80dpwn6'
# )

bot=None

#message = train_bot.train(bot,"hello,what the fuck")
#print message

# msg = location_bot.location(bot, "บ้านป๋าเปรม")
# print msg

# text = u"วันนี้อยากได้ตั๋วไปเชียงใหม่".encode('utf-8')
# message = test_wit.parse(bot,text)
# pprint(message)

print dateparser.parse(u'พรุ่งนี้ ไปเที่ยวกัน')
# print dateparser.parse(u'มรืนนี้')
# print dateparser.parse(u'อาทิตย์หน้า')
# print dateparser.parse(u'เมื่อวาน')
# print dateparser.parse(u'เดือนหน้า')
# print dateparser.parse(u'เดือนที่แล้ว')
