# Contributing to BlueShore Technologies

Thank you for your interest in contributing to **BlueShore Technologies**! We welcome contributions from developers of all skill levels.

---

## Code of Conduct

This project adheres to the Contributor Covenant [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, please include:
- A clear, descriptive title
- Steps to reproduce the behavior
- Expected vs. actual results
- Environment details (OS, Python version, Browser)

### Requesting Features

Feature requests are welcome! Please provide:
- A clear explanation of the proposed feature
- Use cases and benefits to the platform
- Any design considerations or architectural impacts

### Submitting Pull Requests

1. **Fork the Repository** and create your branch from `main`:
   ```bash
   git checkout -b feature/my-amazing-feature
   ```
2. **Set Up Local Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. **Ensure Code Quality & Tests Pass**:
   ```bash
   python manage.py check
   python manage.py makemigrations --check
   python manage.py test
   ```
4. **Commit Changes**: Use clear, descriptive commit messages adhering to Conventional Commits:
   ```bash
   git commit -m "feat: add new lead qualification filter to CRM"
   ```
5. **Push and Open a Pull Request** against the `main` branch.

---

## Coding Guidelines

- **Python Style**: Follow PEP 8 guidelines.
- **Django Conventions**: Keep business logic in models or services; keep views concise.
- **Security**: Never commit API keys, passwords, or `.env` files.
- **Testing**: Add unit tests for any new features or bug fixes in `apps/<app_name>/tests.py`.
