from rest_framework.validators import ValidationError
from urllib.parse import urlparse


def validate_video_link(value):
    parsed_url = urlparse(value)


    if not (parsed_url.scheme and parsed_url.path):
        raise ValidationError("Ссылка некорректна.")
    if (
        "youtube.com" not in parsed_url.hostname
        and "youtu.be" not in parsed_url.hostname
    ):
        raise ValidationError("Разрешены только ссылки на youtube.com.")