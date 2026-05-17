# Photo Album Management (Django)

This project is a production-ready Django photo album manager prepared for deployment to Render and using Cloudinary for media storage.

Key features
- Class-based views for all CRUD operations
- Role-based access control using Django auth (owners + staff)
- Cloudinary-backed media storage (no local media in production)
- PostgreSQL support via `DATABASE_URL` environment variable

Local setup

1. Create virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Create a `.env` file (see `.env.example`) and set:
- `DJANGO_SECRET_KEY`
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
- Optionally `DATABASE_URL` for PostgreSQL

3. Run migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Deployment notes
- Render: use `gunicorn photo_album_project.wsgi` as the start command. Provide environment variables in the Render dashboard. Ensure `DATABASE_URL` is set from the provisioned Postgres.
- Cloudinary: set credentials in environment variables; the code uses `django-cloudinary-storage`.

What I completed
- Full Django project scaffold with `albums` app, CBVs, RBAC mixins, Cloudinary integration in settings, templates, `requirements.txt`, and a `README.md`.
