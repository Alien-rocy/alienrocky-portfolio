# AlienR portfolio redesign: notes

## What changed
- `Templates/base.html` (new): shared head/SEO/nav/footer. `index.html`, `projects.html`, `project_detail.html` extend it.
- `Templates/index.html`: single-page home (Home, Projects, About, Skills, Achievements, Contact).
- `static/assets/portfolio.css` / `portfolio.js`: design system and behaviour (replaces the inline CSS/JS).
- `web/portfolio_data.py`: all featured projects, stack, skills and achievements text. Edit facts here.
- `web/context_processors.py` (registered in settings): exposes socials/email to every template.
- `web/views.py`: `/about` and `/contact` (GET) now redirect to `/#about` and `/#contact`.
  Contact POST still saves a `ContactMessage` and emails you, but a failed email no longer
  loses the message or breaks the form; invalid input returns field errors (HTTP 400).
- Old `Index.html`, `About.html`, `contact.html` were replaced (see your original ZIP if needed).
  The names were also changed to lowercase, which the views already expected (matters on Linux).

## Things you need to supply
- **LinkedIn**: set env var `PORTFOLIO_LINKEDIN_URL` (or edit `SITE["linkedin"]`). Links appear automatically.
- **Project screenshots**: add `static/img/projects/studentpal.webp`, `camply.webp`, `serveflow.webp`
  (jpg/png also work, ~1600x1000). Until then a labelled placeholder shows.
- Project `live` / `github` URLs in `portfolio_data.py` (buttons only render when set).
- Confirm the details marked in `portfolio_data.py`, especially StudentPal's tech tags/status and the Camply "built" list.

## Deploy
`python manage.py collectstatic` then reload the PythonAnywhere web app.

## Dashboard
- `Templates/dashboard/base_dashboard.html` is the shared shell (sidebar, header, theme toggle, mobile drawer);
  every dashboard page, `message_detail.html`, `testimonials.html` and `login.html` now extend or share it.
- Styles: `static/assets/dashboard.css`. Script: `static/assets/dashboard.js` (replaces the old one, which targeted elements that didn't exist).
- Overview now shows real data only: counts, approved vs pending reviews, 5 latest messages, reviews awaiting approval.
  The hard-coded "3" notification badge and missing avatar images were removed.
- Security fix: `message_detail` and `testimonials_view` now require login (they were public before).
- Tables become stacked cards below 700px. Delete buttons ask for confirmation.

## Dynamic featured projects (new)
- The home page projects now come from the database (`Project.featured=True`), and each card links to `/projects/<id>/`.
- New `Project` fields: `featured`, `status`, `tech_stack` (comma separated), `highlights` (one per line).
  Edit them in the dashboard (Projects → Add/Edit). Upload the screenshot there too.
- **Run `python manage.py migrate`.** Migration `0006` adds the fields and creates StudentPal, Camply and ServeFlow
  as featured projects (or just features them if you already added one with the same title).
- The stack section now uses self-hosted inline icons (no external icon CDN).
