from .portfolio_data import SITE


def site(request):
    """Expose shared site details (socials, email) to every template."""
    return {"site": SITE}
