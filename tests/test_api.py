import pytest
from unittest import mock
from hypothesis import given, strategies as st

from blackboard.api import BlackboardSession
from blackboard.blackboard import BBCourse

@given(bbcourse=st.from_type(BBCourse))
def test_my_api(bbcourse):
    with mock.patch('pytest_tiny_api_client._api_call') as api_call:
        api_call.return_value = bbcourse.model_dump()
        s = BlackboardSession("http://blackboard.example.org/api/v{version}", cookies=None)
        api_course = s.fetch_courses(course_id='CO2023')
        assert api_course == bbcourse
