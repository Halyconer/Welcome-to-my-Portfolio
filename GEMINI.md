# Gemini Assistant Guidelines

This document provides instructions for the Gemini AI assistant to ensure its contributions align with the project's standards and my workflow preferences.

## Core Directive

**Do not make any changes to the codebase unless explicitly instructed to do so.**

Before making any modifications—including writing, replacing, or deleting files—please describe the change you propose and await explicit confirmation to proceed.

## Project Context

- **Purpose:** This is a personal portfolio website.
- **Frontend:** Static HTML, CSS, and JavaScript.
- **Backend:** A Python Flask application (`/backend`) that controls a Yeelight smart bulb.

## Common Commands

Here are the preferred commands for common development tasks:

- **Install Backend Dependencies:** `pip install -r backend/requirements.txt`
- **Run Backend Server:** `python backend/app.py`
- **Run Backend Tests:** `python -m pytest backend/test_app.py`
- **Check Frontend Formatting:** `pnpm lint`
- **Format Frontend Code:** `pnpm format`
