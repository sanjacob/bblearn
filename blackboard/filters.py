"""
Client-side result filters for the Blackboard API
"""

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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import fnmatch
from dataclasses import dataclass
from collections.abc import Sequence
from typing import Any, Optional, Callable, TypeVar, Generic

from .blackboard import BBMembership, BBAttachment


def _filter(f, items, search, *,
            blacklist: Sequence | None = None,
            whitelist: Sequence | None = None):
    """
    Filter a list of items by a whitelist or blacklist

    :param items: The sequence containing the items to filter
    :param f: A function that processes the item in the sequence before filtering
              This can be useful for filtering by attribute
    :param search: A search function
    :param blacklist: Items from this list will be removed from the sequence
    :param whitelist: Only items in this list will be allowed in the sequence
    """
    filter_f = None
    if f is None:
        f = lambda x: x

    if whitelist is not None:
        filter_f = lambda x: search(f(x), whitelist)
    elif blacklist is not None:
        filter_f = lambda x: not search(f(x), blacklist)

    return filter(filter_f, items)


T = TypeVar('T')


@dataclass
class BWFilter(Generic[T]):
    """Represents a blacklist/whitelist filter.

    If a whitelist exists it will take precedence.
    """
    blacklist: Optional[list[T]] = None
    whitelist: Optional[list[T]] = None

    def filter(self, f: Callable[[Any], T], items: Sequence[Any]):
        """
        Filters a list of items with either a blacklist or whitelist.

        :param f: A function that can process the items on the list before comparing
                  to the filters. This is specially useful when filtering by a member
                  rather than the object itself
        :param items: A list of items to use the filter onn
        """
        return _filter(f, items, lambda x, seq: x in seq,
                       blacklist=self.blacklist, whitelist=self.whitelist)

    def filter_wc(self, f: Callable[[Any], T], items: Sequence[Any]):
        """
        The same as filter except items are matched with wildcards.

        :see `filter`:
        """
        return _filter(f, items, lambda x, seq: any(fnmatch.fnmatch(s, x) for s in seq),
                       blacklist=self.blacklist, whitelist=self.whitelist)


@dataclass
class BBAttachmentFilter:
    """Groups different kinds of filters that the user may apply to attachments"""
    mime_types: BWFilter

    def filter(self, items: Sequence[BBAttachment]):
        return self.mime_types.filter_wc(lambda x: x.mimeType, items)


@dataclass
class BBMembershipFilter:
    """Groups different kinds of filters that the user may apply to content"""
    data_sources: BWFilter
    min_year: Optional[int] = None

    def filter(self, items: Sequence[BBMembership]):
        if self.min_year is not None:
            # Allow items without a creation date to go through
            items = [m for m in items if
                     m.created is None or m.created.year >= self.min_year]
        return self.data_sources.filter(lambda x: x.dataSourceId, items)
