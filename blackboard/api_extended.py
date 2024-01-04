"""
Blackboard API Extended.

an extension of the Blackboard REST API
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

from typing import Any

from .blackboard import BBCourse
from .api import BlackboardSession
from .filters import BBMembershipFilter


class BlackboardExtended(BlackboardSession):
    """An extension of `BlackboardSession` which adds unofficial features
    on top of it for convenience and ease of use.
    These extensions may be combining two or more steps into one when
    fetching data from the API, or filtering results.
    """

    def ex_fetch_courses(self, *, result_filter: BBMembershipFilter | None = None,
                         **kwargs: Any) -> list[BBCourse]:
        """Fetch all the user's courses and their details"""
        courses = []

        memberships = self.fetch_user_memberships(**kwargs)

        if result_filter is not None:
            memberships = result_filter.filter(memberships)

        for ms in memberships:
            if ms.availability:
                private = False

                assert ms.courseId is not None

                try:
                    course = self.fetch_courses(course_id=ms.courseId)
                except ValueError as e:  # soon to change
                    private = str(e) == 'Private course'
                    # log please
                    raise e

                # mypy does not know result of calling API
                assert isinstance(course, BBCourse)
                course = course.model_copy(update={'created': ms.created})

                if not private:
                    courses.append(course)

        return courses
