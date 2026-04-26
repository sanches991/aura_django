from django import template
from django.utils.translation import get_language

register = template.Library()


@register.filter
def get_translated(obj, field):
    """
    Возвращает значение поля на активном языке.
    Для ru берёт основное поле (field).
    Для en/ky ищет поле field_en / field_ky и
    при пустом значении возвращает русскую версию.

    Использование в шаблоне:
        {{ category|get_translated:"name" }}
        {{ dish|get_translated:"description" }}
    """
    lang = (get_language() or 'ru')[:2]
    if lang != 'ru':
        translated = getattr(obj, f'{field}_{lang}', '') or ''
        if translated.strip():
            return translated
    return getattr(obj, field, '')
