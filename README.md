# College Complaint & Suggestion Box Portal

A full-stack Django portal for collecting complaints and suggestions from students and managing them via an admin dashboard.

## Features
- Student complaint/suggestion submission form
- Notice board for announcements and resolved complaints
- Admin login and dashboard
- Search and category/status filters
- Delete and status update support
- CSV export for complaint records
- Bootstrap-based responsive UI

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install django
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure
- `portal/` — models, views, forms, templates, and URLs
- `static/` — CSS and JavaScript assets
- `templates/` — shared reusable base template

## Notes
- The portal uses SQLite by default.
- Update the `SECRET_KEY` and debug settings for production deployment.
