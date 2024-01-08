"""
Blackboard Model Classes
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

from enum import Enum
from typing import Any
from datetime import datetime

from pydantic import BaseModel, field_validator, ConfigDict
from pathvalidate import sanitize_filename


class ImmutableModel(BaseModel):
    """Model with const attributes."""
    model_config = ConfigDict(frozen=True)


class BBLocale(ImmutableModel):
    force: bool = False


class BBDurationType(str, Enum):
    """Blackboard Course Duration Type."""

    Continuous = 'Continuous'
    DateRange = 'DateRange'
    FixedNumDays = 'FixedNumDays'
    Term = 'Term'
    Other = '__bblearn_other'

    @classmethod
    def _missing_(cls, value: Any) -> 'BBDurationType':
        return cls.Other


class BBDuration(ImmutableModel):
    type: BBDurationType | None = None


class BBEnrollment(ImmutableModel):
    type: str | None = None


class BBProctoring(ImmutableModel):
    secureBrowserRequiredToTake: bool = False
    secureBrowserRequiredToReview: bool = False
    webcamRequired: bool = False


class BBFile(ImmutableModel):
    """Blackboard File."""

    fileName: str | None = None


class BBAttachment(ImmutableModel):
    """Blackboard File Attachment."""

    id: str | None = None
    fileName: str | None = None
    mimeType: str | None = None


class BBLink(ImmutableModel):
    """Blackboard Link."""

    href: str | None = None
    rel: str | None = None
    title: str | None = None
    type: str | None = None


class BBAvailable(str, Enum):
    Yes = 'Yes'
    Term = 'Term'
    No = 'No'
    Disabled = 'Disabled'
    PartiallyVisible = 'PartiallyVisible'
    Other = '__bblearn_other'

    @classmethod
    def _missing_(cls, value: Any) -> 'BBAvailable':
        return cls.Other

    def __bool__(self) -> bool:
        return self not in (BBAvailable.No, BBAvailable.Disabled)


class BBAvailability(ImmutableModel):
    available: BBAvailable | None = None
    allowGuests: bool = False
    adaptiveRelease: dict[str, str] = {}
    duration: BBDuration | None = None

    def __bool__(self) -> bool:
        return bool(self.available)


class BBMembership(ImmutableModel):
    """Blackboard Membership. Represents relation between student and course."""

    id: str | None = None
    userId: str | None = None
    courseId: str | None = None
    dataSourceId: str | None = None
    created: datetime | None = None
    modified: datetime | None = None
    availability: BBAvailability | None = None
    courseRoleId: str | None = None
    lastAccessed: datetime | None = None
    childCourseId: str | None = None


class BBResourceType(str, Enum):
    """Different resource types on Blackboard."""

    Folder = 'x-bb-folder'
    File = 'x-bb-file'
    Document = 'x-bb-document'
    ExternalLink = 'x-bb-externallink'
    ToolLink = 'x-bb-toollink'
    Turnitin_Assignment = 'x-turnitin-assignment'
    BLTIPlacement_Portal = 'x-bb-bltiplacement-Portal'
    Assignment = 'x-bb-assignment'
    Asmt_Test_Link = 'x-bb-asmt-test-link'
    Syllabus = 'x-bb-syllabus'
    CourseLink = 'x-bb-courselink'
    Blankpage = 'x-bb-blankpage'
    Lesson = 'x-bb-lesson'
    Other = '__bblearn_other'

    @classmethod
    def _missing_(cls, value: Any) -> 'BBResourceType':
        return cls.Other


class BBContentHandler(ImmutableModel):
    id: BBResourceType | None = None
    url: str | None = None
    file: BBFile | None = None
    gradeColumnId: str | None = None
    groupContent: bool | None = None
    targetId: str | None = None
    targetType: str | None = None
    placementHandle: str | None = None
    assessmentId: str | None = None
    proctoring: BBProctoring | None = None

    @field_validator('id', mode='before')
    @classmethod
    def trim_resource_type(cls, v: str) -> str:
        if v is None:
            return BBResourceType.Other

        return v.replace('resource/', '')

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BBResourceType):
            return self.id == other
        elif isinstance(other, str):
            return self.id == BBResourceType(other)
        elif isinstance(other, BBContentHandler):
            return super().__eq__(other)
        return False

    def __str__(self) -> str:
        return str(self.id)


class BBCourseContent(ImmutableModel):
    """Blackboard Content."""

    id: str | None = None
    title: str | None = None
    body: str | None = None
    created: datetime | None = None
    modified: datetime | None = None
    position: int = 0
    hasChildren: bool = False
    launchInNewWindow: bool = False
    reviewable: bool = False
    availability: BBAvailability | None = None
    contentHandler: BBContentHandler | None = None
    links: list[BBLink] = []
    hasGradebookColumns: bool = False
    hasAssociatedGroups: bool = False

    def __str__(self) -> str:
        """Title of the course content."""
        return self.title or 'Untitled'

    @property
    def title_path_safe(self) -> str:
        """Return a path safe version of the title."""
        return sanitize_filename(self.title or 'Untitled',
                                 replacement_text='_') or 'Untitled'


class BBContentChild(BBCourseContent):
    """Blackboard Content Child."""

    body: str | None = None
    parentId: str | None = None


class BBCourse(ImmutableModel):
    """BlackboardCourse. Represents an academic course."""

    id: str | None = None
    courseId: str | None = None
    name: str | None = None
    description: str | None = None
    created: datetime | None = None
    modified: datetime | None = None
    organization: bool = False
    ultraStatus: str | None = None
    closedComplete: bool = False
    availability: BBAvailability | None = None
    enrollment: BBEnrollment | None = None
    locale: BBLocale | None = None
    externalAccessUrl: str | None = None

    @property
    def code(self) -> str | None:
        """Parse course code."""
        if self.name:
            code_split = self.name.split(' : ', 1)
            return code_split[0]
        return None

    @property
    def title(self) -> str | None:
        """Parse course title."""
        if self.name:
            name_split = self.name.split(' : ', 1)[-1].split(',')
            return sanitize_filename(name_split[0], replacement_text='_')
        return None
