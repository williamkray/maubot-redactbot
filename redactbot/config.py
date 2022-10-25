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
from typing import List, Union, Dict, Any
import re

from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper

class Config(BaseProxyConfig):

    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("rooms")
        helper.copy("permitted_mime")


class ConfigError(Exception):
    pass
