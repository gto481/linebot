# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the daddy License.

"""bot.models.messages module."""

from __future__ import unicode_literals

from abc import ABCMeta

class BotMessage(with_metaclass(ABCMeta, Base)):
        """Abstract Base Class of Message."""

    def __init__(self, id=None, **kwargs):
        """__init__ method.
        :param str id: Message ID
        :param kwargs:
        """
        super(Message, self).__init__(**kwargs)

        self.type = None
        self.id = id

class BotTextMessage(Message):
    """TextMessage.
    https://devdocs.line.me/en/#text-message
    Message object which contains the text sent from the source.
    """

    def __init__(self, id=None, text=None, **kwargs):
        """__init__ method.
        :param str id: Message ID
        :param str text: Message text
        :param kwargs:
        """
        super(TextMessage, self).__init__(id=id, **kwargs)

        self.type = 'text'
        self.text = text
