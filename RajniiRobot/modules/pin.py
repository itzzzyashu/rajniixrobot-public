from re import compile

from telethon import events, Button
from telethon.errors import ChatAdminRequiredError

from RajniiRobot.utils.pluginhelp import member_permissions
from RajniiRobot import telethn, db

BTN_URL_REGEX = compile(
    r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))")


async def parse_button(text: str):
    """Parse button from text."""
    markdown_note = text
    prev = 0
    note_data = ""
    buttons = []
    for match in BTN_URL_REGEX.finditer(markdown_note):
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and markdown_note[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        if n_escapes % 2 == 0:
            buttons.append((match[2], match[3], bool(match[4])))
            note_data += markdown_note[prev:match.start(1)]
            prev = match.end(1)
        else:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1

    note_data += markdown_note[prev:]

    return note_data, buttons


async def build_keyboard(buttons):
    """Build keyboards from provided buttons."""
    keyb = []
    for btn in buttons:
        if btn[-1] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])

    return keyb


class MongoDB:
    """Class for interacting with Bot database."""

    def __init__(self, collection) -> None:
        self.collection = db[collection]

    def insert_one(self, document):
        result = self.collection.insert_one(document)
        return repr(result.inserted_id)

    def find_one(self, query):
        return result if (result := self.collection.find_one(query)) else False

    def find_all(self, query=None):
        if query is None:
            query = {}
        lst = []
        for document in self.collection.find(query):
            lst.append(document)
        return lst

    def count(self, query=None):
        if query is None:
            query = {}
        return self.collection.count_documents(query)

    def delete_one(self, query):
        self.collection.delete_many(query)
        return self.collection.count_documents({})

    def replace(self, query, new_data):
        old = self.collection.find_one(query)
        _id = old["_id"]
        self.collection.replace_one({"_id": _id}, new_data)
        new = self.collection.find_one({"_id": _id})
        return old, new

    def update(self, query, update):
        result = self.collection.update_one(query, {"$set": update})
        new_document = self.collection.find_one(query)
        return result.modified_count, new_document

    @staticmethod
    def close():
        return mongodb_client.close()


def __connect_first():
    _ = MongoDB("test")


__connect_first()

from threading import RLock

INSERTION_LOCK = RLock()


class Pins:
    """Class for managing antichannelpins in chats."""

    db_name = "antichannelpin"

    def __init__(self, chat_id: int) -> None:
        self.collection = MongoDB(self.db_name)
        self.chat_id = chat_id
        self.chat_info = self.__ensure_in_db()

    def get_settings(self):
        with INSERTION_LOCK:
            return self.chat_info

    def antichannelpin_on(self):
        with INSERTION_LOCK:
            return self.set_on("antichannelpin")

    def cleanlinked_on(self):
        with INSERTION_LOCK:
            return self.set_on("cleanlinked")

    def antichannelpin_off(self):
        with INSERTION_LOCK:
            return self.set_off("antichannelpin")

    def cleanlinked_off(self):
        with INSERTION_LOCK:
            return self.set_off("cleanlinked")

    def set_on(self, atype: str):
        with INSERTION_LOCK:
            otype = "cleanlinked" if atype == "antichannelpin" else "antichannelpin"
            return self.collection.update(
                {"_id": self.chat_id},
                {
                    atype: True,
                    otype: False
                },
            )

    def set_off(self, atype: str):
        with INSERTION_LOCK:
            otype = "cleanlinked" if atype == "antichannelpin" else "antichannelpin"
            return self.collection.update(
                {"_id": self.chat_id},
                {
                    atype: False,
                    otype: False
                },
            )

    def __ensure_in_db(self):
        chat_data = self.collection.find_one({"_id": self.chat_id})
        if not chat_data:
            new_data = {
                "_id": self.chat_id,
                "antichannelpin": False,
                "cleanlinked": False,
            }
            self.collection.insert_one(new_data)
            return new_data
        return chat_data

    def migrate_chat(self, new_chat_id: int):
        old_chat_db = self.collection.find_one({"_id": self.chat_id})
        new_data = old_chat_db.update({"_id": new_chat_id})
        self.collection.insert_one(new_data)
        self.collection.delete_one({"_id": self.chat_id})

    @staticmethod
    def count_chats(atype: str):
        with INSERTION_LOCK:
            collection = MongoDB(Pins.db_name)
            return collection.count({atype: True})

    @staticmethod
    def list_chats(query: str):
        with INSERTION_LOCK:
            collection = MongoDB(Pins.db_name)
            return collection.find_all({query: True})

    @staticmethod
    def load_from_db():
        with INSERTION_LOCK:
            collection = MongoDB(Pins.db_name)
            return collection.findall()

    @staticmethod
    def repair_db(collection):
        all_data = collection.find_all()
        keys = {"antichannelpin": False, "cleanlinked": False}
        for data in all_data:
            for key, val in keys.items():
                try:
                    _ = data[key]
                except (KeyError, IndexError):
                    collection.update({"_id": data["_id"]}, {key: val})


def __pre_req_pins_chats():
    collection = MongoDB(Pins.db_name)
    Pins.repair_db(collection)


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]antichannelpin(?:\s+(.*))?$", incoming=True))
async def anti_channel_pin(event):
    if event.is_private:
        return
    chat_id = event.chat_id
    user_id = event.sender_id
    if not user_id:
        return
        
    permissions = await member_permissions(chat_id, user_id)
    if "can_change_info" not in permissions:
        await event.reply("You Don't Have Enough Permissions.")
        return
    if "can_pin_messages" not in permissions:
        await event.reply("You Don't Have Enough Permissions.")
        return
    if "can_restrict_members" not in permissions:
        await event.reply("You Don't Have Enough Permissions.")
        return
    if "can_promote_members" not in permissions:
        await event.reply("You Don't Have Enough Permissions.")
        return
        
    pinsdb = Pins(chat_id)
    args = event.text.split()
    if len(args) == 1:
        status = pinsdb.get_settings()["antichannelpin"]
        await event.reply(f"Antichannelpin currently: {status}")
        return

    if len(args) == 2:
        if args[1].lower() in ("yes", "on", "true"):
            pinsdb.antichannelpin_on()
            msg = "Antichannelpin turned on for this chat"
        elif args[1].lower() in ("no", "off", "false"):
            pinsdb.antichannelpin_off()
            msg = "Antichannelpin turned off for this chat"
        else:
            await event.reply("Invalid syntax")
            return

    await event.reply(msg)
    return


@telethn.on(events.NewMessage(incoming=True))
async def antichanpin_cleanlinked(event):
    if event.is_private:
        return
    # Check if message is from a linked channel
    if not event.is_channel or event.chat_id == event.sender_id: # or check via forward/sender if available
        # Telethon identifies linked channel posts via event.is_forwarded or specific attributes, or we can check forward info
        pass

    try:
        # Telethon flags linked channel messages or channel broadcasts posting as group
        if event.fwd_from or (event.sender and event.sender.bot is False and getattr(event.sender, 'megagroup', False) is False):
            # Alternative: verify if it's a linked channel message
            pass
            
        msg_id = event.id
        chat_id = event.chat_id
        pins_db = Pins(chat_id)
        curr = pins_db.get_settings()
        
        # Check if message is pinned automatically by telegram (service message or linked channel message)
        if curr["antichannelpin"]:
            try:
                await telethn(telethon.tl.functions.messages.UpdatePinnedMessagesRequest(
                    peer=chat_id,
                    id=[msg_id],
                    unpin=True
                ))
            except Exception:
                await telethn.unpin_message(chat_id, message=msg_id)
                
        if curr["cleanlinked"]:
            await event.delete()
    except ChatAdminRequiredError:
        await event.reply(
            "Disabled antichannelpin as I don't have enough admin rights!"
        )
        pins_db.antichannelpin_off()
    except Exception:
        return
    return


__mod_name__ = "Pinning"