"""Blackboard REST API exceptions."""

# Copyright (C) 2023, Jacob Sánchez Pérez

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

from typing import Any, NoReturn
from tiny_api_client import APIStatusError


class BBBadRequestError(Exception):
    pass


class BBUnauthorizedError(Exception):
    pass


class BBForbiddenError(Exception):
    pass


def status_handler(client: Any, status_code: Any, response: Any) -> NoReturn:
    match status_code:
        case 400:
            raise BBBadRequestError()
        case 401:
            raise BBUnauthorizedError()
        case 403:
            raise BBForbiddenError()
        case _:
            raise APIStatusError(status_code)
