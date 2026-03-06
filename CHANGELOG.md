[[_TOC_]]

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Add vim/neovim integration instructions to README (#205)
- Add VSCode integration instructions to README (#222)
- Adopt flake8-tidy-imports to enforce O.1.5 (#223)
- Add fallbacks to `_get_application_import_names` (#234)
- Make format command (#221)

### Changed
- Drop Python 3.7 support (#218)

### Fixed
- Fix formatting files with unicode (#242)
- Fix acknowledge when run on multiple files (#244)

## [0.4.9] - 2026-02-03

### Fixed
- Work around "No module named 'pkg_resources'" by pinning setuptools to <82 (#275)

## [0.4.8] - 2026-01-23

### Fixed
- Pin black to version that supports Python < 3.10 still (#262)

### Changed
- Update project version (#230)

## [0.4.7] - 2025-07-10

No changes documented for this release.

## [0.4.6] - 2024-06-12

### Fixed
- Fix command being over aggressive (#185)
- Bump the patch version number (#184)

### Added
- Ignore documentation errors in Sphinx config (#183)

### Security
- Bump nokogiri from 1.16.2 to 1.16.5 in /docs (#180)
- Bump rexml from 3.2.5 to 3.2.8 in /docs (#181)

## [0.4.5] - 2024-05-02

### Added
- Add `nps` as short command (#154)
- Ignore F401 for init.py files (#173)

### Changed
- Remove 3.7 testing (#179)
- Remove @rtzoeller from notification list (#178)

### Security
- Bump nokogiri from 1.14.3 to 1.16.2 in /docs (#163)

## [0.4.4] - 2023-10-17

### Added
- Also ignore D102 Missing docstring in public method in tests (#148)

### Changed
- Update poetry lock and reformat (#147)

## [0.4.3] - 2023-10-13

### Added
- Also allow flat tests to ignore missing docstrings (#146)

## [0.4.2] - 2023-10-10

### Added
- Add support for Python 3.12 (#143)
- Document fix subcommand (#127)

### Changed
- Update poetry lock and reformat (#144)
- Bump package patch version since last release did not (#145)
- Use native gh tooling to raise pr (#138)
- Switch the pat used to create the PR to enable PR checks (#140)
- Update lock poetry version (#130)
- Enable running lock action on demand (#131)
- Testing if this makes PRs run checks (#135)

## [0.4.1] - 2023-04-27

### Added
- Ignore missing docstrings in methods in "tests" dir "test_*.py" (#120)
- Adding documentation about BLK100 issue in D.1.12, add Visual Studio dir to .gitignore (#117)

### Changed
- Remove D.1.12 from Coding-Conventions, bump black min version to 23.1 (#119)
- Add check to skip update poetry lock action on forks (#108)

### Fixed
- Fix acknowledge comments (#126)

### Security
- Bump activesupport from 6.0.4.6 to 6.0.6.1 in /docs (#105)
- Bump nokogiri from 1.13.10 to 1.14.3 in /docs (#123)

## [0.4.0] - 2023-01-20

### Added
- Recommend Google Style for DocStrings (#88)

### Fixed
- Fix comments (#101)
- Fix no split submodule imports (#102)

### Changed
- Update Poetry Lock (#100)

## [0.3.0] - 2023-01-09

### Changed
- Bump flake8 to 5.x (#98)
- Fix up tooling (#99)

## [0.2.0] - 2022-12-08

### Changed
- Drop 3.6 support (#96)
- Disallow black 22.10.0 because the initial macOS wheels had the wrong architecture (#95)
- Remove `alexweav` from bot @-mention list (#91)

### Security
- Bump nokogiri from 1.13.6 to 1.13.9 in /docs (#93)
- Bump nokogiri from 1.13.9 to 1.13.10 in /docs (#94)

## [0.1.17] - 2023-10-12

### Changed
- Testing release pipeline

## [0.1.15] - 2023-10-10

### Changed
- Cherry-pick explicitly recommending Google style

## [0.1.14.4] - 2023-10-09

### Changed
- Cherry-pick: Tests may skip doc-strings

## [0.1.13] - 2022-10-12

### Fixed
- Pin importlib-metadata for python 3.7 and under (#92)

### Changed
- Use black profile with isort to reduce manual work (#87)
- Change pr commenter tooling (#89)
- Add tkrebes to tag list for convention changes (#90)

### Security
- Bump nokogiri from 1.13.4 to 1.13.6 in /docs (#85)
- Bump tzinfo from 1.2.9 to 1.2.10 in /docs (#86)

## [0.1.12] - 2022-05-09

### Fixed
- Fix bug in "fix --aggressive" (#84)

## [0.1.11] - 2022-05-02

### Added
- Add fix command (#80)

### Changed
- Refactor linting utilities to own submodule (#82)

### Security
- Bump nokogiri from 1.12.5 to 1.13.3 in /docs (#78)
- Update Gemfile.lock (#79)
- Bump nokogiri from 1.13.3 to 1.13.4 in /docs (#81)

## [0.1.10] - 2022-02-03

### Changed
- Treat global mutables as global vars (#75)
- Be more lenient on dependency versioning by using >= (#77)

## [0.1.9] - 2021-11-17

### Fixed
- Fix some acknowledge corner cases (#74)

## [0.1.8] - 2021-11-15

### Added
- Add --aggressive flag to acknowledge subcommand (#72)

### Changed
- Change links to fully qualified (#48)
- Run PR on multiplatform and multi Python version (#53)
- Document Release Instructions (#54)
- Update README.md (#56)
- Update pipeline templates (#59)
- Fix #55 by using smarkets style (#57)
- Improve multiline statement handling (#67)
- Update deps (#73)

### Fixed
- Avoid index errors when input file is empty (#66)
- Suppression handle unicode files (#69)
- Better handle when acknowledging violations will cause reformat (#72)
- Coding-Conventions.md: fix 404 for black (#71)

### Security
- Bump nokogiri from 1.11.1 to 1.11.5 in /docs (#62)
- Bump rexml from 3.2.4 to 3.2.5 in /docs (#61)
- Bump addressable from 2.7.0 to 2.8.0 in /docs (#63)
- Bump nokogiri from 1.11.1 to 1.12.5 in /docs (#68)

## [0.1.7.0] - 2021-10-20

Release pipeline was broken, retrigger push to pypi.org

## [0.1.6.0] - 2021-10-20

### Fixed
- Default acknowledge script to using UTF-8 encoding on source files (#69)

## [0.1.5.1] - 2021-09-08

### Fixed
- Fix auto-suppression handling blank files (#66)

### Added
- Add hacking to rejected plugins (#50)
- Reject flake8-commas (#51)
- Reject flake8-isort (#52)

## [0.1.5.0] - 2021-02-12

### Added
- Add flake8-import-order to rules being evaluated (#49)

## [0.1.4] - 2021-02-02

### Added
- Add acknowledge-existing-errors command to allow for easy adoption or upgrade to newest version

## [0.1.3] - 2021-02-01

### Added
- Add pep8-naming plugin

## [0.1.2] - 2021-01-07

### Changed
- Use admin PAT to bypass checks when bumping Poetry version (#39)

## [0.1.1] - 2021-01-06

### Changed
- Bump the package version to 0.1.0-alpha since the 0.1.0 release already exists

## [0.1.0] - 2021-01-06

### Added
- Initial Release 🚀

[Unreleased]: https://github.com/ni/python-styleguide/compare/v0.4.9...main
[0.4.9]: https://github.com/ni/python-styleguide/compare/v0.4.8...v0.4.9
[0.4.8]: https://github.com/ni/python-styleguide/compare/v0.4.7...v0.4.8
[0.4.7]: https://github.com/ni/python-styleguide/compare/v0.4.6...v0.4.7
[0.4.6]: https://github.com/ni/python-styleguide/compare/v0.4.5...v0.4.6
[0.4.5]: https://github.com/ni/python-styleguide/compare/v0.4.4...v0.4.5
[0.4.4]: https://github.com/ni/python-styleguide/compare/v0.4.3...v0.4.4
[0.4.3]: https://github.com/ni/python-styleguide/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/ni/python-styleguide/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/ni/python-styleguide/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/ni/python-styleguide/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/ni/python-styleguide/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/ni/python-styleguide/compare/v0.1.13...v0.2.0
[0.1.17]: https://github.com/ni/python-styleguide/compare/v0.1.15...v0.1.17
[0.1.15]: https://github.com/ni/python-styleguide/compare/v0.1.14.4...v0.1.15
[0.1.14.4]: https://github.com/ni/python-styleguide/compare/v0.1.13...v0.1.14.4
[0.1.13]: https://github.com/ni/python-styleguide/compare/v0.1.12...v0.1.13
[0.1.12]: https://github.com/ni/python-styleguide/compare/v0.1.11...v0.1.12
[0.1.11]: https://github.com/ni/python-styleguide/compare/v0.1.10...v0.1.11
[0.1.10]: https://github.com/ni/python-styleguide/compare/v0.1.9...v0.1.10
[0.1.9]: https://github.com/ni/python-styleguide/compare/v0.1.8...v0.1.9
[0.1.8]: https://github.com/ni/python-styleguide/compare/0.1.4...v0.1.8
[0.1.7.0]: https://github.com/ni/python-styleguide/compare/0.1.4...0.1.7.0
[0.1.6.0]: https://github.com/ni/python-styleguide/compare/0.1.5.1...0.1.6.0
[0.1.5.1]: https://github.com/ni/python-styleguide/compare/0.1.5.0...0.1.5.1
[0.1.5.0]: https://github.com/ni/python-styleguide/compare/0.1.4...0.1.5.0
[0.1.4]: https://github.com/ni/python-styleguide/compare/0.1.3...0.1.4
[0.1.3]: https://github.com/ni/python-styleguide/compare/v0.1.2...0.1.3
[0.1.2]: https://github.com/ni/python-styleguide/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/ni/python-styleguide/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/ni/python-styleguide/releases/tag/v0.1.0
