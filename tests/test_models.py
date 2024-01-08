import pytest
from hypothesis import given, strategies as st

from blackboard.blackboard import (
    BBFile,
    BBDurationType,
    BBAvailable,
    BBAvailability,
    BBResourceType,
    BBContentHandler,
    BBCourseContent,
    BBCourse
)


def test_bb_durationtype():
    assert BBDurationType('Continuous') == BBDurationType.Continuous
    assert BBDurationType('DateRange') == BBDurationType.DateRange
    assert BBDurationType('FixedNumDays') == BBDurationType.FixedNumDays
    assert BBDurationType('Term') == BBDurationType.Term
    assert BBDurationType('ARandomDurationType') == BBDurationType.Other

def test_bb_available():
    assert BBAvailable('No') == BBAvailable.No
    assert BBAvailable('Yes') == BBAvailable.Yes
    assert BBAvailable('Term') == BBAvailable.Term
    assert BBAvailable('Disabled') == BBAvailable.Disabled
    assert BBAvailable('PartiallyVisible') == BBAvailable.PartiallyVisible
    assert BBAvailable('ARandomAvailableValue') == BBAvailable.Other

@pytest.mark.parametrize('available', ('UnexpectedValue', 'NotReal'))
def test_bb_available_other(available: str):
    assert BBAvailable(available) == BBAvailable.Other

@pytest.mark.parametrize('available', ('Yes', 'Term', 'PartiallyVisible' 'UnexpectedValue'))
def test_bb_available_yes(available: str):
    assert BBAvailable(available)

@pytest.mark.parametrize('available', ('No', 'Disabled'))
def test_bb_available_no(available: str):
    assert not BBAvailable(available)

@given(st.from_type(BBAvailable))
def test_bb_availability_bool(available):
    assert bool(BBAvailability(available=available)) == bool(available)

def test_bb_resourcetype():
    assert BBResourceType("x-bb-file") == BBResourceType.File
    assert BBResourceType("x-bb-folder") == BBResourceType.Folder
    assert BBResourceType("x-bb-document") == BBResourceType.Document
    assert BBResourceType("x-bb-externallink") == BBResourceType.ExternalLink
    assert BBResourceType("x-bb-unhandled-resource") == BBResourceType.Other

@given(st.from_type(BBResourceType))
def test_bb_contenthandler_id(res_type):
    assert BBContentHandler(id=f"resource/{res_type}").id == res_type

@given(st.from_type(BBResourceType))
def test_bb_contenthandler_str(res_type):
    assert str(BBContentHandler(id=res_type)) == str(res_type)

@given(st.from_type(BBResourceType))
def test_bb_contenthandler_eq_resourcetype(res_type):
    b = BBContentHandler(id=res_type)
    assert b == res_type.value
    assert b == res_type

@given(st.text(min_size=1))
def test_bb_coursecontent_str(title):
    b = BBCourseContent(title=title)
    assert str(b) == title

def test_bb_coursecontent_str_untitled():
    b = BBCourseContent(title='')
    assert str(b) == 'Untitled'

def test_bb_coursecontent_title_path():
    assert BBCourseContent(title="unsafe<path.txt").title_path_safe == "unsafe_path.txt"
    assert BBCourseContent(title="unsafe\\path.txt").title_path_safe == "unsafe_path.txt"
    assert BBCourseContent(title="../../unsafe<path.txt").title_path_safe == ".._.._unsafe_path.txt"

def test_bb_course_code():
    assert BBCourse(name="CO2345 : Information Security ").code == "CO2345"

def test_bb_course_title():
    assert BBCourse(name="CO2345 : Information Security, 2023 ").title == "Information Security"