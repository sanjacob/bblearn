"""
Test the Blackboard API
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

from unittest import mock
from hypothesis import given, strategies as st

from blackboard.api import BlackboardSession
from blackboard.blackboard import (BBCourse, BBCourseContent,
                                   BBContentChild, BBAttachment)


API_URL = "http://blackboard.example.org/api/v{version}"


@given(bbcourse=st.from_type(BBCourse))
def test_fetch_courses(bbcourse):
    with mock.patch('pytest_tiny_api_client._api_call') as api_call:
        api_call.return_value = bbcourse.model_dump()
        s = BlackboardSession(API_URL, cookies=None)
        assert s.fetch_courses(course_id='...') == bbcourse


@given(bbcourse=st.lists(st.from_type(BBCourse)))
def test_fetch_courses_list(bbcourse):
    with mock.patch('pytest_tiny_api_client._api_call') as api_call:
        api_call.return_value = [x.model_dump() for x in bbcourse]
        s = BlackboardSession(API_URL, cookies=None)
        assert s.fetch_courses() == bbcourse


@given(bbcoursecontent=st.lists(st.from_type(BBCourseContent)))
def test_fetch_contents(bbcoursecontent):
    with mock.patch('pytest_tiny_api_client._api_call') as api_call:
        api_call.return_value = [x.model_dump() for x in bbcoursecontent]
        s = BlackboardSession(API_URL, cookies=None)
        assert s.fetch_contents(
            course_id='...', content_id='...'
        ) == bbcoursecontent


@given(bbcontentchild=st.lists(st.from_type(BBContentChild)))
def test_fetch_content_children(bbcontentchild):
    with mock.patch('pytest_tiny_api_client._api_call') as api_call:
        api_call.return_value = [x.model_dump() for x in bbcontentchild]
        s = BlackboardSession(API_URL, cookies=None)
        assert s.fetch_content_children(
            course_id='...', content_id='...'
        ) == bbcontentchild


@given(bbattachment=st.from_type(BBAttachment))
def test_fetch_file_attachments(bbattachment):
    with mock.patch('pytest_tiny_api_client._api_call') as api_call:
        api_call.return_value = bbattachment.model_dump()
        s = BlackboardSession(API_URL, cookies=None)
        assert s.fetch_file_attachments(
            course_id='...', content_id='...'
        ) == bbattachment


@given(bbattachment=st.lists(st.from_type(BBAttachment)))
def test_fetch_file_attachments_list(bbattachment):
    with mock.patch('pytest_tiny_api_client._api_call') as api_call:
        api_call.return_value = [x.model_dump() for x in bbattachment]
        s = BlackboardSession(API_URL, cookies=None)
        assert s.fetch_file_attachments(
            course_id='...', content_id='...', attachment_id='...'
        ) == bbattachment
