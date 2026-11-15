"""
Content for the AlienR portfolio home page.

Everything shown on the public site that is NOT stored in the database lives
here, so facts can be corrected in one place. Only include things that are true:
- Featured projects now live in the database: manage them in the dashboard.
- Dates: leave `date` empty unless verified.
"""
import os

SITE = {
    "name": "Agbaje Peter Oluwatimilehin",
    "brand": "AlienR",
    "title": "Software Engineer | Backend & Web Developer",
    "email": "rockytim5205@gmail.com",
    "github": "https://github.com/rockytiM-5205",
    "x": "https://x.com/alienrocky5205",
    "whatsapp": "https://wa.me/2348129733237",
    # LinkedIn URL was not found in the original project. Set the environment
    # variable PORTFOLIO_LINKEDIN_URL (or edit here) and the links appear
    # automatically; while empty, no LinkedIn link is rendered (no dead links).
    "linkedin": os.environ.get("PORTFOLIO_LINKEDIN_URL", ""),
    "url": os.environ.get("SITE_URL", "https://oluwatimilehinagbaje.vercel.app").rstrip("/"),
}

# (group, header icon, [(label, simple-icons slug or None, fallback icon id)])
# Brand logos load from the jsDelivr simple-icons CDN; if it is unreachable the
# fallback icon (inline SVG in partials/icons.html) is shown instead.
STACK = [
    ("Backend", "i-server", [("Python", "python", "i-t-python"), ("Django", "django", "i-t-django"), ("Django REST Framework", None, "i-t-api"), ("PostgreSQL", "postgresql", "i-db")]),
    ("Frontend", "i-code", [("HTML", "html5", "i-t-html"), ("CSS", "css3", "i-t-css"), ("JavaScript", "javascript", "i-t-js")]),
    ("Tools", "i-branch", [("Git", "git", "i-branch"), ("GitHub", "github", "i-github"), ("Postman", "postman", "i-t-send"), ("Docker", "docker", "i-t-box")]),
    ("Deployment", "i-cloud", [("Render", "render", "i-server"), ("Netlify", "netlify", "i-t-globe"), ("Cloudinary", "cloudinary", "i-t-upload"), ("Vercel", "vercel", "i-t-triangle")]),
]

SKILL_GROUPS = [
    ("01", "Backend Development", ["Python", "Django", "Django REST Framework", "API development"]),
    ("02", "Frontend Development", ["HTML", "CSS", "JavaScript"]),
    ("03", "Databases", ["PostgreSQL", "Relational database design"]),
    ("04", "Tools & Version Control", ["Git", "GitHub", "Postman", "Docker"]),
    ("05", "Deployment & Infrastructure", ["Render", "Netlify", "Cloudinary", "Vercel"]),
]

# date: only fill in when verified.
ACHIEVEMENTS = [
    {
        "title": "InnovateX Ecobank 2026",
        "org": "Ecobank",
        "role": "Backend Team Member",
        "text": "Backend team member for the InnovateX Ecobank 2026 programme.",
        "date": "2026",
    },
    {
        "title": "Youth Credit Scoring & Alternative Risk Engine",
        "org": "Internal team pitch",
        "role": "",
        "text": "The team's pitch for this project won the internal pitch.",
        "date": "",
        "badge": "Won",
    },
    {
        "title": "DevCareer × Nomba Build Phase",
        "org": "DevCareer × Nomba",
        "role": "Hackathon participant",
        "text": "Took part in the Build Phase of the hackathon.",
        "date": "",
    },
    {
        "title": "Team Decode, NACOS AAUA",
        "org": "NACOS, Adekunle Ajasin University",
        "role": "",
        "text": "Placed 4th with LinkDecoder AI.",
        "date": "",
        "badge": "4th place",
    },
    {
        "title": "GitHub Achievements",
        "org": "GitHub",
        "role": "",
        "text": "Earned the Pull Shark achievement.",
        "date": "",
    },
]
