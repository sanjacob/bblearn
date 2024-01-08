"""
Blackboard API.

an interface to make Blackboard REST API calls on a session basis
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

import logging
import requests
from typing import Any
from requests.cookies import RequestsCookieJar

from tiny_api_client import api_client, get

from .blackboard import (BBMembership, BBCourse, BBCourseContent,
                         BBContentChild, BBAttachment)


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
_logger.addHandler(logging.NullHandler())


@api_client(timeout=12)
class BlackboardSession:
    """Represents a user session in Blackboard."""

    def __init__(self, url: str, *, cookies: RequestsCookieJar):
        """
        :param url: The URL of the blackboard API to use
        :param cookies: A `RequestsCookieJar` authorized to browse the API
        """
        self._url = url
        self._cookies = cookies
        self._username: str

    @property
    def username(self) -> str:
        """Username field used for API requests."""
        if self._username is None:
            username = self.fetch_users(user_id='me')['userName']
            self._username = f'userName:{username}'
        return self._username

    # WEBDAV DOWNLOAD

    @get("{webdav_url}", stream=True, json=False, use_api=False)
    def download_webdav(self, response: requests.Response) -> requests.Response:
        """Downloads an arbitrary webdav file"""
        return response

    # API CALLS
    # https://developer.blackboard.com/portal/displayApi

    # announcements #

    @get("/announcements/{announcement_id}")
    def fetch_announcements(self, response: Any) -> Any:
        """Return a list of System Announcements.

        :param announcement_id: Get a System Announcement.
        """
        return response

    # attendance #

    @get("/courses/{course_id}/meetings")
    def fetch_course_meetings(self, response: Any) -> Any:
        """Return a list of course meetings for a given course id.

        :param course_id: The course or organization ID.
        """
        return response

    @get("/courses/{course_id}/meetings/downloadUrl")
    def fetch_attendance_data_download_url(self, response: Any) -> Any:
        """Generate Download URL for Attendance Data.

        :param course_id: The course or organization ID.
        """
        return response

    @get("/courses/{course_id}/meetings/users/{user_id}")
    def fetch_attendance_records_by_user_id(self, response: Any) -> Any:
        """Return a list of Course Meeting Attendance for a given user id
        regardless of courses and meetings.

        :param course_id: The course or organization ID.
        :param user_id: The user ID.
        """
        return response

    @get("/courses/{course_id}/meetings/{meeting_id}")
    def fetch_course_meeting(self, response: Any) -> Any:
        """Return a Course Meeting for the given meeting Id.

        :param course_id: The course or organization ID.
        :param meeting_id:
        """
        return response

    @get("/courses/{course_id}/meetings/{meeting_id}/users/{user_id}")
    def fetch_attendance_records_by_meeting_id(self, response: Any) -> Any:
        """Return a Course Meeting Attendance information
        for the given meeting and user Id.

        :param course_id: The course or organization ID.
        :param meeting_id:
        :param user_id: The user ID.
        """
        return response

    # calendar #

    @get("/calendars/")
    def fetch_calendar(self, response: Any) -> Any:
        """Get the list of calendars viewable by the user.

        All users can request a list of calendars viewable to them.
        """
        return response

    @get("/calendars/items/{calendar_item_type}/{calendar_item_id}")
    def fetch_calendar_items(self, response: Any) -> Any:
        """Get a course calendar item.

        :param calendar_item_type: One of (Course, GradebookColumn, Institution,
            OfficeHours, Personal).
        :param calendar_item_id:
        """
        return response

    # content #

    @get("/courses/{course_id}/contents/{content_id}")
    def fetch_contents(self, response: Any) -> list[BBCourseContent]:
        """List top-level content items in a course.

        :param course_id: The course or organization ID.
        :param content_id: The Content ID.
        """
        return [BBCourseContent(**content) for content in response]

    @get("/courses/{course_id}/contents/{content_id}/children")
    def fetch_content_children(self, response: Any) -> list[BBContentChild]:
        """List all child content items directly beneath another content item.

        This is only valid for content items that are allowed to have children.

        :param course_id: The course or organization ID.
        :param content_id: The Content ID.
        """
        return [BBContentChild(**child) for child in response]

    # content file attachments #

    @get("/courses/{course_id}/contents/{content_id}/attachments/{attachment_id}")
    def fetch_file_attachments(self, response: Any
                               ) -> list[BBAttachment] | BBAttachment:
        """Get the file attachment meta data associated to the Content Item.

        or Get the file attachment meta data by an attachment ID.

        :param course_id: The course or organization ID.
        :param content_id: The Content ID.
        :param attachment_id:
        """
        if isinstance(response, list):
            return [BBAttachment(**a) for a in response]
        else:
            return BBAttachment(**response)

    @get("/courses/{course_id}/contents/{content_id}/"
         "attachments/{attachment_id}/download",
         json=False, stream=True)
    def download(self, response: Any) -> Any:
        """Download the contents of a Content Item.

        :param course_id: The course or organization ID.
        :param content_id: The Content ID.
        :param attachment_id:
        """
        return response

    # content group assignments #

    @get("/courses/{course_id}/contents/{content_id}/groups/{group_id}")
    def fetch_content_groups(self, response: Any) -> Any:
        """Return a list of content group associations for the specified content.

        :param course_id: The course or organization ID.
        :param content_id: The Content ID.
        :param group_id: The group ID.
        """
        return response

    # content resources #

    @get("/courses/{course_id}/resources/{resource_id}")
    def fetch_course_resources(self, response: Any) -> Any:
        """Return a list of the top-level course resources.

        or Load a Course Resource by Id.

        :param course_id: The course or organization ID.
        :param resource_id: The xythos resource ID.
        """
        return response

    @get("/courses/{course_id}/resources/{resource_id}/children")
    def fetch_course_resource_children(self, response: Any) -> Any:
        """
        Return a list of Course Resources that are children of the specified Resource.

        :param course_id: The course or organization ID.
        :param resource_id: The xythos resource ID.
        """
        return response

    # content review #

    @get("/courses/{course_id}/contents/{content_id}/users/{user_id}/reviewStatus")
    def fetch_review_status(self, response: Any) -> Any:
        """Obtain the review status for a content item.

        This endpoint will only fetch the reviewStatus if the corresponding content
        was previously marked as reviewable.

        :param course_id: The course or organization ID.
        :param content_id: The Content ID.
        :param user_id: The user ID.
        """
        return response

    # course announcements #

    @get("/courses/{course_id}/announcements/{announcement_id}")
    def fetch_course_announcements(self, response: Any) -> Any:
        """Return a list of Course Announcements or Get a Course Announcement.

        :param course_id: The course or organization ID.
        :param announcement_id:
        """
        return response

    # course assessments #

    @get("/courses/{course_id}/assessments/{assessment_id}/questions/{question_id}")
    def fetch_questions(self, response: Any) -> Any:
        """Get the list of questions for an Ultra Assessment
        or Get a question by Id from it.

        :param course_id: The course or organization ID.
        :param assessment_id:
        :param question_id:
        """
        return response

    # course categories #

    @get("/catalog/categories/{category_type}/{category_id}")
    def fetch_category(self, response: Any) -> Any:
        """Return a list of categories of the provided type (course or organization).
        / Return the category corresponding the provided type
        (course or organization) and ID.

        :param category_type: One of (Course, Organization).
        :param category_id:
        """
        return response

    @get("/catalog/categories/{category_type}/{category_id}/courses/{course_id}")
    def fetch_memberships(self, response: Any) -> Any:
        """
        Get courses associated with the provided category.

        :param category_type: One of (Course, Organization).
        :param category_id:
        """
        return response

    @get("/catalog/categories/{category_type}/{parent_id}/children")
    def fetch_child_categories(self, response: Any) -> Any:
        """Return a list of categories which are children of the category...

        corresponding to the provided type (course or organization) and Id

        :param category_type: One of (Course, Organization).
        :param parent_id:
        """
        return response

    @get("/courses/{course_id}/categories")
    def fetch_categories(self, response: Any) -> Any:
        """Get categories associated with the provided course.

        :param course_id: The course or organization ID.
        """
        return response

    # course grade attempts #

    @get("/courses/{course_id}/gradebook/attempts/"
         "{attempt_id}/files/{attempt_file_id}")
    def fetch_attempt_file_metadata(self, response: Any) -> Any:
        """Get the list of file metadata for a Submission
        associated to the course and attempt.

        Get the file metadata for a Student Submission associated to the course
        and attempt.

        :param course_id: The course or organization ID.
        :param attempt_id:
        :param attempt_file_id:
        """
        return response

    @get("/courses/{course_id}/gradebook/attempts/"
         "{attempt_id}/files/{attempt_file_id}/download")
    def download_attempt_file_metadata(self, response: Any) -> Any:
        """Download the contents of the file for a Student Submission.

        :param course_id: The course or organization ID.
        :param attempt_id:
        :param attempt_file_id:
        """
        return response

    # course grade notations #

    @get("/courses/{course_id}/gradebook/gradeNotations/{grade_notation_id}")
    def fetch_grade_notations(self, response: Any) -> Any:
        """Return a list of grade notations. / Return a specific grade notation.

        :param course_id: The course or organization ID.
        :grade_notation_id:
        """
        return response

    # course gradebook categories #

    @get("/courses/{course_id}/gradebook/categories/{category_id}")
    def fetch_gradebook_categories(self, response: Any) -> Any:
        """Return a list of gradebook categories in a particular course.

        / Return the details of a gradebook category.

        :param course_id: The course or organization ID.
        :param category_id: the ID of the category to return
        """
        return response

    # course grades #

    @get("/courses/{course_id}/gradebook/schemas/{schema_id}")
    def fetch_grade_schemas(self, response: Any) -> Any:
        """Return a list of grade schemas associated with the specified course.

        / Load the grade schema associated with the specified course and schema Id.

        :param course_id: The course or organization ID.
        :param schema_id: The grade schema ID.
        """
        return response

    @get("/courses/{course_id}/gradebook/columns/{column_id}", version=2)
    def fetch_grade_columns(self, response: Any) -> Any:
        """Return a list of grade columns. / Load a specific grade column.

        :param course_id: The course or organization ID.
        :param column_id: The grade column ID.
        """
        return response

    @get("/courses/{course_id}/gradebook/columns/{column_id}/attempts/{attempt_id}",
         version=2)
    def fetch_column_attempts(self, response: Any) -> Any:
        """Return a list of attempts associated with the specified grade column.

        / Load the grade column attempt for the specified id.

        :param course_id: The course or organization ID.
        :param column_id: The grade column ID.
        :param attempt_id:
        """
        return response

    @get("/courses/{course_id}/gradebook/columns/{column_id}/users/{user_id}",
         version=2)
    def fetch_column_grades(self, response: Any) -> Any:
        """Return a list of grades associated with the specified grade column.

        / Load the grade column grade for a specific user.

        :param course_id: The course or organization ID.
        :param column_id: The grade column ID.
        :param user_id: The user ID.
        """
        return response

    @get("/courses/{course_id}/gradebook/columns/{column_id}/users/lastChanged",
         version=2)
    def fetch_column_grade_last_changed(self, response: Any) -> Any:
        """Load the grade column grade with the maximum change index.

        :param course_id: The course or organization ID.
        :param column_id: The grade column ID.
        """
        return response

    @get("/courses/{course_id}/gradebook/users/{user_id}", version=2)
    def fetch_user_grades(self, response: Any) -> Any:
        """Load the course grades for a specific user.

        :param course_id: The course or organization ID.
        :param user_id: The user ID.
        """
        return response

    # course grading periods #

    @get("/courses/{course_id}/gradebook/periods/{period_id}")
    def fetch_grading_periods(self, response: Any) -> Any:
        """Return a list of grading periods. / Return a specific grading period.

        :param course_id: The course or organization ID.
        :param period_id:
        """
        return response

    # course group users #

    @get("/courses/{course_id}/groups/{group_id}/users/{user_id}", version=2)
    def fetch_group_memberships(self, response: Any) -> Any:
        """Return a list of group memberships objects for the specified group.

        / Loads a group membership in the specified group.

        :param course_id: The course or organization ID.
        :param group_id: The group ID.
        :param user_id: The user ID.
        """
        return response

    # course groups #

    @get("/courses/{course_id}/groups/{group_id}", version=2)
    def fetch_groups(self, response: Any) -> Any:
        """Return a list of all top-level groups in the specified course.

        / Load a group in the specified course.

        :param course_id: The course or organization ID.
        :param group_id: The group ID.
        """
        return response

    @get("/courses/{course_id}/groups/sets/{group_id}", version=2)
    def fetch_group_sets(self, response: Any) -> Any:
        """Return a list of all groupsets / Load a groupset in the specified course.

        :param course_id: The course or organization ID.
        :param group_id: The group ID.
        """
        return response

    @get("/courses/{course_id}/groups/sets/{group_id}/groups", version=2)
    def fetch_group_set_children(self, response: Any) -> Any:
        """Return a list of all groups within a groupset.

        :param course_id: The course or organization ID.
        :param group_id: The group ID.
        """
        return response

    # course memberships #

    @get("/courses/{course_id}/users/{user_id}")
    def fetch_course_memberships(self, response: Any) -> Any:
        """Return a list of user memberships for the specified course or organization.

        / Load a user membership in the specified course.

        :param course_id: The course or organization ID.
        :param user_id: The user ID.
        """
        return response

    @get("/users/{user_id}/courses")
    def fetch_user_memberships(self, response: Any) -> list[BBMembership]:
        """Return a list of course and organization memberships for the specified user.

        :param user_id: The user ID.
        """
        return [BBMembership(**memb) for memb in response]

    # courses #

    @get("/courses/{course_id}/children/{child_course_id}")
    def fetch_course_children(self, response: Any) -> Any:
        """Return a list of course cross-listings.

        / Load a specific course cross-listing.

        :param course_id: The course or organization ID.
        :param child_course_id: The course or organization ID.
        """
        return response

    @get("/courses/{course_id}/crossListSet")
    def fetch_cross_list_set(self, response: Any) -> Any:
        """Return the course cross-listing set for the specified course.

        This will return any and all parent/child associations regardless of
        the specified course being a parent or child course.
        The result will be empty if the specified course is not cross-listed.

        :param course_id: The course or organization ID.
        """
        return response

    @get("/courses/{course_id}/tasks/{task_id}")
    def fetch_task(self, response: Any) -> Any:
        """Check the status of a queued task associated with a Course.

        Returns 200 unless task is complete.

        :param course_id: The course or organization ID.
        :param task_id:
        """
        return response

    @get("/courses/{course_id}", version=3)
    def fetch_courses(self, response: Any) -> BBCourse | list[BBCourse]:
        """Return a list of courses and organizations.

        / Loads a specific course or organization.

        :param course_id: The course or organization ID.
        """
        if isinstance(response, list):
            return [BBCourse(**course) for course in response]
        else:
            return BBCourse(**response)

    # data sources #

    @get("/dataSources/{data_source_id}")
    def fetch_data_sources(self, response: Any) -> Any:
        """Return a list of data sources.

        :param data_source_id: The data source ID.
        """
        return response

    # institutional hierarchy #

    @get("/courses/{course_id}/nodes")
    def fetch_associated_nodes(self, response: Any) -> Any:
        """Obtain a list of nodes to which a given course is directly associated.

        :param course_id: The course or organization ID.
        """
        return response

    @get("/institutionalHierarchy/nodes/{node_id}")
    def fetch_nodes(self, response: Any) -> Any:
        """Return the Top-level institutional hierarchy nodes.

        / Return the institutional hierarchy node corresponding the provided ID.

        :param node_id: The node ID.
        """
        return response

    @get("/institutionalHierarchy/nodes/{node_id}/children")
    def fetch_node_children(self, response: Any) -> Any:
        """Return the children of the institutional hierarchy node corresponding...

        to the provided ID.

        :param node_id: The node ID.
        """
        return response

    @get("/institutionalHierarchy/nodes/{node_id}/courses")
    def fetch_node_course_associations(self, response: Any) -> Any:
        """Return a list of node-course relationships for the specified node.

        :param node_id: The node ID.
        """
        return response

    # lti #

    @get("/lti/placements/{placement_id}")
    def fetch_placements(self, response: Any) -> Any:
        """Return a list of LTI placements.

        / Returns the LTI placement with the specified Id.

        :param placement_id:
        """
        return response

    @get("/lti/domains/{domain_id}")
    def fetch_domain_config(self, response: Any) -> Any:
        """Return the list of LTI domain configs.

        / This endpoint returns the LTI domain config with the specified Id.

        :param domain_id:
        """
        return response

    # performance dashboard #

    @get("/courses/{course_id}/performance/contentReviewStatus")
    def fetch_performance_review_status(self, response: Any) -> Any:
        """List the content review statuses for all the users enrolled in a course.

        :param course_id: The course or organization ID.
        """
        return response

    # proctoring #

    @get("/proctoring/services/{service_id}")
    def fetch_proctoring_services(self, response: Any) -> Any:
        """Return a list of proctoring service.

        / Return the proctoring service with the specified Id.

        :param service_id:
        """
        return response

    # roles #

    @get("/courseRoles/{role_id}")
    def fetch_course_roles(self, response: Any) -> Any:
        """Return a list of course roles. / Return a single course role.

        :param role_id: The course role ID.
        """
        return response

    @get("/institutionRoles/{role_id}")
    def fetch_institution_roles(self, response: Any) -> Any:
        """Return a list of institution roles. / Load a specific institution role.

        :param role_id: The institution role ID.
        """
        return response

    @get("/systemRoles/{role_id}")
    def fetch_system_roles(self, response: Any) -> Any:
        """Return a list of system roles. / Get a specific system role by roleId.

        :param role_id: The System Role ID.
        """
        return response

    # sessions #

    @get("/sessions")
    def fetch_sessions(self, response: Any) -> Any:
        """List active user sessions in Learn."""
        return response

    # SIS logs #

    @get("/logs/sis/dataSets/{id}")
    def fetch_sis_logs(self, response: Any) -> Any:
        """Return a list of SIS Integration logs.

        :param id: dataSetUid of the integration
        """
        return response

    # system #

    @get("/system/policies/privacy")
    def fetch_policies(self, response: Any) -> Any:
        """Return the links to the Blackboard and Institution privacy policies."""
        return response

    @get("/system/tasks/{task_id}")
    def fetch_system_task(self, response: Any) -> Any:
        """Get the background task by the given task Id.

        :param task_id:
        """
        return response

    @get("/system/version")
    def fetch_version(self, response: Any) -> Any:
        """Get the current Learn server version."""
        return response

    # terms #

    @get("/terms/{term_id}")
    def fetch_terms(self, response: Any) -> Any:
        """Return a list of terms. / Load a term.

        :param term_id: The term ID.
        """
        return response

    # uploads #

    # users #

    @get("/users/{user_id}")
    def fetch_users(self, response: Any) -> Any:
        """Return a list of users. / Load a user.

        Properties returned will depend on the caller's entitlements.

        :param user_id: The user ID.
        """
        return response

    # Get Users Avatar
    # TODO: Handle this API call (HTTP header)
    @get("/users/{user_id}/avatar")
    def fetch_avatar(self, response: Any) -> Any:
        """Get a user avatar image.

        The response: Any is an HTTP redirect rather than image raw data.
        It is up to the caller of the api to follow the redirect
        and download the image.

        Not yet implemented.
        :param user_id: The user ID.
        """
        raise NotImplementedError("API has not implemented this method yet.")
        return response

    @get("/users/{user_id}/observees")
    def fetch_observees(self, response: Any) -> Any:
        """Return a list of users being observed by a given user.

        :param user_id: The user ID.
        """
        return response

    @get("/users/{user_id}/observers")
    def fetch_observers(self, response: Any) -> Any:
        """Return a list of users observing a given user.

        :param user_id: The user ID.
        """
        return response

    @get("/users/{user_id}/sessions")
    def fetch_current_active_user(self, response: Any) -> Any:
        """Display active session information for a specific user.

        :param user_id: The user ID.
        """
        return response

    @property
    def url(self) -> str:
        """API URL."""
        return self._url
