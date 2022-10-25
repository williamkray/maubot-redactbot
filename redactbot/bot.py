# redactbot - A maubot plugin that redacts all files but some whitelisted types.
# Copyright (C) 2019-22 Tulir Asokan. (C) 2022 Sebastian Spaeth
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Type, Tuple, Dict
import time

from attr import dataclass

from mautrix.types import EventType, MessageType, UserID, RoomID
from mautrix.util.config import BaseProxyConfig

from maubot import Plugin, MessageEvent
from maubot.handlers import event

from .config import Config, ConfigError


class RedactBot(Plugin):
    allowed_msgtypes: Tuple[MessageType, ...] = (MessageType.FILE,)

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    async def start(self) -> None:
        await super().start()
        self.on_external_config_update()

    def on_external_config_update(self) -> None:
        self.config.load_and_update()

    @event.on(EventType.ROOM_MESSAGE)
    async def event_handler(self, evt: MessageEvent) -> None:
        if evt.room_id not in self.config['rooms'] or \
           evt.sender == self.client.mxid or \
           evt.content.msgtype not in self.allowed_msgtypes:
            # msg from a room we don't supervise, we did not send
            # ourself or is not in EventType.FILE?
            return
        self.log.debug(f"File {evt.content.body} ({evt.content.info.mimetype}) posted in room {evt.room_id}")
        if evt.content.info.mimetype in self.config['permitted_mime']:
            # Don't do anything for permitted file types.
            self.log.debug(f"This is a permitted file type: {evt.content.info.mimetype}")
            return

        self.log.warning(f"Redacting file {evt.content.body} in room {evt.room_id}")
        power_evt = await self.client.get_state_event(evt.room_id, EventType.ROOM_POWER_LEVELS)
        bot_power = list(power_evt.users.values())[0]
        if bot_power < power_evt.redact:
            self.log.critical(f"MISSING POWER LEVEL IN ROOM {evt.room_id}. I HAVE {bot_power} BUT NEED {power_evt.redact}")
            await evt.reply(f"I am configured to redact your file {evt.content.body} but someone forgot to give me moderator power!")
            return
        await self.client.redact(evt.room_id, evt.event_id)
        await evt.reply(f"I redacted your file {evt.content.body}. No files in here but {self.config['permitted_mime']}.")
        return
