# Contributing Guidelines – Movie Recommendation System

Thank you for your interest in contributing to this project!  
This document explains how to contribute code, documentation, tests, or ideas in a clean and professional way.

---

## 1. How to Contribute

### ✔️ Steps for contribution

| Step | Description                                     |
|------|-------------------------------------------------|
| 1    | Fork this repository to your GitHub account     |
| 2    | Create a new branch for your change             |
| 3    | Implement your modifications                    |
| 4    | Write or update tests if necessary              |
| 5    | Submit a Pull Request (PR) for review           |

### ✔️ Git Commands (example workflow)

```bash
# Clone your fork
git clone https://github.com/<your-username>/movie-recommendation-system.git

# Create a new branch
git checkout -b feature/my-improvement

# Commit your changes
git commit -m "feat: add feature my-improvement"

# Push to your branch
git push origin feature/my-improvement

### 2. Coding Standards

| Topic            | Guideline                                                   |
|------------------|-------------------------------------------------------------|
| Code Style       | Follow PEP‑8 conventions                                    |
| File Organization| Group related modules logically                             |
| Comments         | Keep comments short and meaningful                          |
| Docstrings       | Use Google‑style or PEP‑257 docstrings                      |
| Exceptions       | Raise explicit errors with clear messages                   |
| Logging          | Use the `logging` module instead of print statements        |

3. Testing Requirements
Contributions that modify logic must include tests.
Tests should be placed in:

###  ✔️ Test checklist

| Requirement      | Description                                      |
|------------------|--------------------------------------------------|
| Unit tests       | Validate functions, classes, isolated modules    |
| API tests        | Use FastAPI `TestClient` to test all endpoints   |
| Data tests       | Validate transformations & input schema         |
| ML tests         | Validate model loading & inference consistency   |

### 4. Pull Requests – Good PR Includes

| Item             | Requirement                                        |
|------------------|----------------------------------------------------|
| Description      | Clear explanation of the change                    |
| Motivation       | Why the change is necessary                        |
| Screenshots      | If UI/API output changes                           |
| Tests            | Added or updated, all passing                      |
| Documentation    | Updated if necessary                                |

✔️ PR Naming Convention

feat: new feature
fix: bug fix
docs: documentation improvements
refactor: code refactor
test: test-related changes
perf: performance improvements

5. Code of Conduct

Be respectful and constructive
Keep discussions centered on improving the project
Avoid submitting untested or unrelated code

6. Questions or Suggestions?
If you have ideas, notice bugs, or want to propose changes, feel free to:

Open an Issue on GitHub
Write a Discussion
Submit a small PR for review

We welcome contributions of all sizes!
