# Deploying to Vercel

## 1. Environment variables (Vercel → Project → Settings → Environment Variables)
| Name | Required | Notes |
|---|---|---|
| `DATABASE_URL` | yes | Postgres URL (Neon / Supabase). Prefer the *pooled* connection string. |
| `DJANGO_SECRET_KEY` | strongly | Long random string. The old key was public in git: replace it. |
| `CLOUDINARY_URL` | for uploads | `cloudinary://API_KEY:API_SECRET@CLOUD_NAME`. Vercel can't save files, so dashboard image uploads need this. |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | for email | Gmail address + an App Password. Without them emails are only logged. |
| `CONTACT_RECIPIENT` | optional | Defaults to rockytim5205@gmail.com. |
| `SITE_URL` | optional | Your public URL (canonical + social preview tags). |
| `ALLOWED_HOSTS` | custom domain | Comma separated, e.g. `yourdomain.com,www.yourdomain.com`. `*.vercel.app` is already allowed. |
| `PORTFOLIO_LINKEDIN_URL` | optional | Shows the LinkedIn links. |

## 2. Set up the database (once, from your computer)
```
pip install -r requirements.txt
set DATABASE_URL=postgresql://...        (PowerShell: $env:DATABASE_URL="...")
python manage.py migrate
python manage.py createsuperuser         # this is your dashboard login at /login/
```
Re-run `migrate` after any model change. Vercel does not run migrations for you.

## 3. Deploy
Push to GitHub; Vercel builds automatically. Static files are served directly (no `collectstatic` needed).

## Notes
- Images already inside `media/` are served from the repo. New uploads go to Cloudinary.
- Celery was removed (Vercel has no background workers). Send the newsletter with `python manage.py send_newsletter`.
- Delete, approve and log-out are now POST buttons with CSRF protection; unsubscribe links are signed.
- Run `python manage.py test` before pushing (tests cover public pages, dashboard login, create/delete project, contact, unsubscribe).
- Keep `db.sqlite3` out of git (it holds subscriber emails and messages): `git rm --cached db.sqlite3`.
- Template files must be lowercase (`home.html`): Windows hides case-only renames from git, Vercel's Linux does not.
