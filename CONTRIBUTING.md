# Contributing to MovieObserver

Thank you for considering contributing to MovieObserver! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by its [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

Bug reports help us improve the project. To report a bug:

1. Check if the bug has already been reported in the GitHub Issues.
2. If not, create a new issue with a descriptive title and clear description.
3. Include steps to reproduce the issue, expected behavior, and actual behavior.
4. Add screenshots if applicable.

### Suggesting Enhancements

We welcome suggestions for enhancements:

1. Check if the enhancement has already been suggested in the GitHub Issues.
2. If not, create a new issue with a descriptive title prefixed with "Enhancement:" and a clear description.
3. Explain why this enhancement would be useful.

### Adding New Scrapers

One of the most valuable contributions is adding support for new cinema websites:

1. Fork the repository and create a new branch.
2. Create a new scraper class in `backend/scraper/` by extending the `BaseScraper` class.
3. Implement the required methods, particularly `get_movies_for_date`.
4. Update `scraper_service.py` to include your new scraper.
5. Add tests for your scraper.
6. Submit a pull request.

### Pull Requests

1. Fork the repository and create a branch for your feature.
2. Write clear, commented code following the project's code style.
3. Include tests for your changes.
4. Update documentation as necessary.
5. Submit a pull request with a clear description of the changes.

## Development Setup

See the README.md for detailed setup instructions.

### Backend Development

1. Set up the Python virtual environment and install dependencies.
2. Run the backend with `uvicorn api.main:app --reload`.
3. Run tests with `pytest`.

### Frontend Development

1. Install Node.js dependencies.
2. Run the frontend with `npm run dev`.
3. Run tests with `npm test`.

## Code Style

### Python (Backend)

- Follow PEP 8 guidelines.
- Use meaningful variable and function names.
- Add docstrings for all functions, classes, and modules.
- Format code with Black.

### TypeScript/JavaScript (Frontend)

- Follow the ESLint configuration.
- Use meaningful variable and function names.
- Use TypeScript types appropriately.
- Format code with Prettier.

## Testing

- Write unit tests for backend code using pytest.
- Write unit tests for frontend components using Jest and React Testing Library.

## Documentation

- Keep README.md and other documentation up to date.
- Add comments to your code explaining complex logic.
- Document all API endpoints using FastAPI's documentation features.

## Commit Messages

- Use clear, descriptive commit messages.
- Use the imperative mood ("Add feature" not "Added feature").
- Reference issue numbers when applicable.

## Release Process

The maintainers will handle the release process following semantic versioning.

## Questions?

If you have any questions about contributing, feel free to open an issue or contact the maintainers.

Thank you for contributing to MovieObserver!
