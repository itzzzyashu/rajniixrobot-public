import threading
from sqlalchemy import Column, String
from RajniiRobot.modules.sql import BASE, SESSION


class AIChatBotChats(BASE):
    __tablename__ = "AiChatBotChats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


AIChatBotChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_aichatbot_enabled(chat_id):
    try:
        chat = SESSION.query(AIChatBotChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def add_aichatbot(chat_id):
    with INSERTION_LOCK:
        aichat = SESSION.query(AIChatBotChats).get(str(chat_id))
        if not aichat:
            aichat = AIChatBotChats(str(chat_id))
        SESSION.add(aichat)
        SESSION.commit()


def rem_aichatbot(chat_id):
    with INSERTION_LOCK:
        aichat = SESSION.query(AIChatBotChats).get(str(chat_id))
        if aichat:
            SESSION.delete(aichat)
        SESSION.commit()


def get_all_aichatbot_chats():
    try:
        return SESSION.query(AIChatBotChats.chat_id).all()
    finally:
        SESSION.close()
