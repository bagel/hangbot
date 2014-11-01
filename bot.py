import sys
import os
import asyncio
import json
import hangups


class HangBot(object):
    def __init__(self):
        self.cookie = "cookie"
        self._user_list = None
        self._conv_list = None
        self._auth()
        self._client = hangups.Client(json.load(open(self.cookie, "r")))
        self._client.on_connect.add_observer(self._on_connect)

    def _auth(self):
        hangups.get_auth(lambda: ("xxxxxx@gmail.com", "xxxxxx"), lambda: "", self.cookie)

    def _on_connect(self, initial_data):
        self._user_list = hangups.UserList(
            self._client, initial_data.self_entity, initial_data.entities,
            initial_data.conversation_participants
        )
        self._conv_list = hangups.ConversationList(
            self._client, initial_data.conversation_states, self._user_list,
            initial_data.sync_timestamp
        )
        self.send_message()

    def _on_quit(self):
        future = asyncio.async(self._client.disconnect())
        future.add_done_callback(lambda future: future.result())

    def _on_message_sent(self, f):
        print(f.result())

    def send_message(self):
        #print(self._user_list._user_dict)
        #print(self._conv_list._conv_dict)
        conversation = self._conv_list.get(conv)
        segments = hangups.ChatMessageSegment.from_str(text)
        asyncio.async(
            conversation.send_message(segments)
        ).add_done_callback(self._on_message_sent)
        

if __name__ == "__main__":
    hb = HangBot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hb._client.connect())
    loop.close()
