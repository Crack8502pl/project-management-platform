# Contributing to Project Management Platform

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Development Setup

### Backend Development

1. Clone the repository:
```bash
git clone https://github.com/Crack8502pl/project-management-platform.git
cd project-management-platform/backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements/development.txt
```

4. Set up environment:
```bash
cp ../.env.example ../.env
```

5. Run migrations:
```bash
python manage.py migrate
python manage.py init_roles
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

## Code Style

### Python (Backend)

We follow PEP 8 style guide with some modifications:

- **Line length**: 100 characters
- **Formatter**: Black
- **Import sorting**: isort
- **Linter**: flake8

Format your code before committing:

```bash
# Format with Black
black .

# Sort imports
isort .

# Check with flake8
flake8 .
```

### Code Structure

- Keep functions and methods small and focused
- Use descriptive variable and function names
- Add docstrings to classes and complex functions
- Follow Django best practices

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation changes

### 2. Make Your Changes

- Write clean, readable code
- Follow the code style guidelines
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

Run tests:
```bash
pytest
pytest --cov=apps --cov-report=html
```

Run validation:
```bash
python validate_structure.py
```

### 4. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: description of what you did"
```

Good commit message examples:
- `Add user role management API endpoint`
- `Fix task completion date not being set`
- `Refactor BOM template serializer`
- `Update API documentation for projects`

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Description of what was changed and why
- References to related issues

## Adding New Features

### Adding a New Model

1. Define model in appropriate app's `models.py`
2. Create and run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
3. Register in `admin.py`
4. Create serializer in `serializers.py`
5. Create viewset in `views.py`
6. Add URL route in `urls.py`
7. Write tests
8. Update documentation

### Adding a New API Endpoint

1. Create/update serializer
2. Create/update viewset or view
3. Add URL pattern
4. Test the endpoint
5. Update API documentation

### Adding a Management Command

1. Create file in `apps/<app>/management/commands/`
2. Implement Command class
3. Test the command
4. Document usage

## Testing

### Writing Tests

- Place tests in `tests.py` or `tests/` directory in each app
- Name test files as `test_*.py`
- Use descriptive test names

Example:
```python
def test_create_project_with_valid_data():
    """Test creating a project with valid data."""
    # Test implementation
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest apps/projects/tests.py

# Run with coverage
pytest --cov=apps --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Documentation

- Update README.md for major features
- Add docstrings to new classes and functions
- Update API documentation comments
- Keep CHANGELOG.md updated

## Database Migrations

- Always create migrations for model changes:
```bash
python manage.py makemigrations
```

- Review migration files before committing
- Test migrations in both directions:
```bash
python manage.py migrate
python manage.py migrate <app> <previous_migration>
```

## Code Review Process

1. All changes must go through Pull Request
2. At least one approval required
3. All tests must pass
4. Code must follow style guidelines
5. Documentation must be updated

## Security

- Never commit sensitive data (passwords, keys, tokens)
- Use environment variables for configuration
- Follow Django security best practices
- Report security issues privately

## Questions?

If you have questions:
- Check existing documentation
- Review closed issues and PRs
- Open an issue for discussion
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing! 🎉
