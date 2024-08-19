# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.2] - 2024-08-19

### Fixed
- Error status handler now has correct signature

## [0.3.1] - 2024-08-12

### Changed
- Extended method `ex_fetch_courses` now detects a 403 response
- The package-wide logger is now public

### Added
- Logging was added to the extended api module

## [0.3.0] - 2024-08-11

### Added
- Custom API exceptions when server returns error code

## [0.2.9] - 2024-08-09

### Added
- Session property of initial instance URL without api path

## [0.2.8] - 2024-08-09

### Changed
- Set definitive API root based on documentation

## [0.2.7] - 2024-08-09

### Changed
- Implement `user_id` property rather than `username`

## [0.2.6] - 2024-08-07

### Changed
- Make id mandatory in `BBCourse`, `BBCourseContent`, `BBAttachment`
- Make courseId mandatory in `BBMembership`

## [0.2.5] - 2024-08-05

### Removed
- `BBContentChild` class made redundant

## [0.2.4] - 2024-01-20

### Changed
- `filter_wc` will allow None only in blacklist mode

## [0.2.3] - 2024-01-11

### Changed
- Allow tiny-api-client version to be upgraded

## [0.2.2] - 2024-01-11

### Added
- Add type annotations to filters module

## [0.2.1] - 2024-01-11

### Added
- Add py.typed file to distribution

## [0.2.0] - 2024-01-10

### Added
- Improved tests and formatting

### Changed
- Updated tiny-api-client

## [0.1.0] - 2023-11-23

### Added
- Initial release
