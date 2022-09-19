from django import template
register = template.Library()

@register.filter
def get_thumbnail(image_url, size):
    img_name = image_url.split('/')[2]
    thumb_name = f"{img_name.split('.')[0]}_{size}.{img_name.split('.')[1]}"
    new_url = image_url.replace(img_name, thumb_name)
    return new_url


