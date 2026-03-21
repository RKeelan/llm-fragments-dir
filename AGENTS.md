# AGENTS.md

This file provides guidance to AI coding agents working in this repository.

## Project Overview

llm-fragments-dir is a plugin for [LLM](https://llm.datasette.io/) that loads all text files from a local directory as fragments. It registers a `dir` fragment loader via LLM's plugin hook system (`@llm.hookimpl`). Binary files are skipped using a UTF-8 sniff check.

## Development Setup

```bash
python -m venv venv
source venv/bin/activate
llm install -e '.[test]'
```

## Commands

- **Run all tests:** `pytest .`
- **Run tests with coverage (as CI does):** `python -m pytest --cov=llm_fragments_dir --cov-report=term-missing --cov-fail-under=95`
- **Run a single test:** `pytest tests/test_fragments_dir.py::test_name`

## Architecture

Single-module plugin (`llm_fragments_dir.py`) with no sub-packages. The entry point is registered in `pyproject.toml` under `[project.entry-points.llm]`. The module exposes:

- `register_fragment_loaders` — LLM hook that registers the `"dir"` loader
- `directory_loader` — walks a directory with `os.walk`, filters to UTF-8 files via `is_probably_utf8`, and returns `llm.Fragment` objects
- `is_probably_utf8` — heuristic check reading the first 4KB of a file

## CI

Tests run on Python 3.9–3.13 (Ubuntu) and 3.13 (Windows). Coverage must stay at or above 95%.
