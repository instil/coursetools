# Test Suite for coursetools

This directory contains comprehensive unit tests for the coursetools application using pytest.

## Overview

The test suite covers all major components of the coursetools application:

- **test_app.py** - Tests for the CLI application entry point and argument parsing
- **test_config.py** - Tests for configuration loading and retrieval
- **test_templates.py** - Tests for template loading and management
- **test_repository.py** - Tests for repository creation and file operations
- **conftest.py** - Shared fixtures and test configuration

## Running Tests

### Run all tests:
```bash
pytest
```

### Run with verbose output:
```bash
pytest -v
```

### Run with coverage report:
```bash
pytest --cov=coursetools --cov-report=term-missing
```

### Run specific test file:
```bash
pytest tests/test_app.py
```

### Run specific test class or function:
```bash
pytest tests/test_app.py::TestShowTemplates
pytest tests/test_app.py::TestShowTemplates::test_show_templates_prints_header
```

## Test Coverage

The test suite achieves 100% code coverage across all modules:
- `src/coursetools/app.py`
- `src/coursetools/config.py`
- `src/coursetools/repository.py`
- `src/coursetools/templates.py`

## Test Structure

### Fixtures (conftest.py)
- `temp_dir` - Creates temporary directory for tests
- `mock_template_dir` - Creates mock template directory with test templates
- `mock_config_dir` - Creates mock configuration directory
- `mock_repo_structure` - Creates mock training repository structure

### Test Categories

#### Unit Tests
Test individual functions and methods in isolation:
- Configuration loading and retrieval
- Template discovery and parsing
- Argument parsing

#### Integration Tests
Test interactions between components:
- Full repository creation workflow
- File copying with exclusions
- Template validation with real templates

#### Functional Tests
Test end-to-end functionality:
- CLI command execution
- Template listing
- Repository creation with various scenarios

## Test Design Principles

1. **Isolation** - Tests use temporary directories and mocking to avoid side effects
2. **Comprehensive** - Tests cover happy paths, edge cases, and error conditions
3. **Clear** - Test names describe what is being tested
4. **Fast** - Tests run quickly using in-memory operations where possible
5. **Maintainable** - Tests are organized by module and use shared fixtures

## Adding New Tests

When adding new functionality to coursetools:

1. Add corresponding tests in the appropriate test file
2. Use existing fixtures from `conftest.py` where applicable
3. Follow the existing naming conventions (test_function_name_describes_behavior)
4. Ensure tests are isolated and don't depend on external state
5. Run tests and verify coverage remains at 100%

## Continuous Integration

These tests are designed to run in CI/CD pipelines. The pytest configuration in `pyproject.toml` includes:
- Coverage reporting
- Strict marker and config validation
- HTML coverage reports (output to `htmlcov/`)
