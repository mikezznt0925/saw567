# GitHub API 567 (HW03a / HW03c Mocking)

[![Build Status](https://app.travis-ci.com/mikezznt0925/saw567.svg?branch=HW03a_Mocking)](https://app.travis-ci.com/mikezznt0925/saw567)

This badge shows the build status for the **HW03a_Mocking** branch. All unit tests mock the GitHub API via `unittest.mock`; no real API calls are made during tests.

## Requirements

- Python 3.x
- `pip install -r requirements.txt` (requires `requests`)

## Usage

```bash
python github_api.py
python github_api.py <GitHub_user_id>
```

## Run tests (no GitHub API calls)

```bash
pip install -r requirements.txt
python -m unittest test_github_api -v
```
