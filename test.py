# -*- coding: utf-8 -*-
from chatterbot import ChatBot

chatbot = ChatBot(
    'LineBot',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)
chatbot.train("chatterbot.corpus.thai")

text = unicode(u"เฮโหล")
response = chatbot.get_response(text)
print response.text.encode('utf-8')