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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

from dataclasses import dataclass
from collections.abc import Sequence, Iterable

from bwfilters import BWFilter

from .blackboard import BBMembership, BBAttachment


@dataclass
class BBAttachmentFilter:
    """Filters that the user may apply to attachments"""
    mime_types: BWFilter[BBAttachment]

    def filter(self, items: Sequence[BBAttachment]) -> Iterable[BBAttachment]:
        return self.mime_types.filter_wc(lambda x: x.mimeType, items)


@dataclass
class BBMembershipFilter:
    """Filters that the user may apply to content"""
    data_sources: BWFilter[BBMembership]
    min_year: int | None = None

    def filter(self, items: Sequence[BBMembership]) -> Iterable[BBMembership]:
        if self.min_year is not None:
            # Allow items without a creation date to go through
            items = [m for m in items if
                     m.created is None or m.created.year >= self.min_year]
        return self.data_sources.filter(lambda x: x.dataSourceId, items)
