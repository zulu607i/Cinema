from django import template
import pathlib
from cinema import settings
register = template.Library()

@register.filter
def get_thumbnail(image_url, size):
    img_name = pathlib.Path(image_url)
    thumb_name = f"{settings.MEDIA_URL}{img_name.stem}_{size}{img_name.suffix}"
    return thumb_name


