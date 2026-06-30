# GitHub Copilot Code Review Instructions

## Overview
These instructions guide code review analysis for pull requests, focusing on security, style consistency, and documentation completeness.

## Review Checklist

### 1. Security Issues
- **Input Validation**: Verify that user inputs, external data, and file contents are properly validated and sanitized
- **Injection Attacks**: Check for SQL injection, command injection, and code injection vulnerabilities
- **Sensitive Data**: Ensure no hardcoded secrets, API keys, passwords, or sensitive credentials are exposed
- **Dependency Vulnerabilities**: Flag any deprecated or vulnerable dependencies
- **Access Control**: Verify proper authentication and authorization checks are in place
- **Error Handling**: Check that error messages don't leak sensitive information
- **File Operations**: Ensure safe file handling with proper path validation and permissions checks

### 2. Style Consistency
- **Naming Conventions**: Check that variables, functions, and classes follow project naming conventions
- **Documentation**: Verify docstrings are present in the public API and follow project conventions
- **Consistency with Existing Code**: Ensure new code matches the style and patterns used elsewhere in the project

### 3. Changelog Updates
- **Behavioral Changes**: Verify that any changes to existing functionality are documented in CHANGELOG.md
- **Public API Changes**: Ensure additions, modifications, or removals of public APIs are logged
- **Breaking Changes**: Flag breaking changes and verify they are clearly documented
- **New Features**: Confirm new features are added to the changelog
- **Bug Fixes**: Check that significant bug fixes are documented
- **Versioning**: Verify that version updates align with semantic versioning principles

## Reporting
When reviewing code, provide clear feedback indicating:
- Which category the issue falls under (Security, Style, or Changelog)
- The specific concern or violation
- A suggestion for resolution where applicable
- Severity level (critical, high, medium, low)
