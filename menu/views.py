from pathlib import PurePosixPath

from django.db.models import Count, Prefetch, Q
from django.views.generic import TemplateView, View
from django.shortcuts import render

from .models import Category, Dish, Ingredient, RestaurantInfo, Greeting, InfoRule, Fine, SocialLinks


RESPONSIVE_IMAGE_WIDTHS = (480, 768, 1200)


def attach_responsive_image_sources(categories):
    for category in categories:
        for dish in category.dishes.all():
            dish.image_srcset = build_image_srcset(dish)
    return categories


def build_image_srcset(dish):
    if not dish.image:
        return ''

    storage = dish.image.storage
    original = PurePosixPath(dish.image.name)
    variant_dir = original.parent / 'optimized'
    srcset = []

    for width in RESPONSIVE_IMAGE_WIDTHS:
        variant_name = str(variant_dir / f'{original.stem}-{width}.webp')
        if storage.exists(variant_name):
            srcset.append(f'{storage.url(variant_name)} {width}w')

    return ', '.join(srcset)


class InfoView(TemplateView):
    """Стартовая страница — ознакомление с рестораном."""
    template_name = 'menu/info.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['restaurant_info'] = RestaurantInfo.get_instance()
        ctx['greetings'] = Greeting.objects.all()
        ctx['rules'] = InfoRule.objects.all()
        ctx['fines'] = Fine.objects.all()
        ctx['social_links'] = SocialLinks.get_instance()
        return ctx


class MenuView(View):
    """Главная страница с меню."""

    def get(self, request):
        ingredients_qs = Ingredient.objects.order_by('order', 'id')

        dishes_qs = (
            Dish.objects
            .filter(is_available=True)
            .order_by('order', 'id')
            .prefetch_related(Prefetch('ingredients', queryset=ingredients_qs))
        )

        categories = list(
            Category.objects
            .annotate(dish_count=Count('dishes', filter=Q(dishes__is_available=True)))
            .filter(dish_count__gt=0)
            .prefetch_related(Prefetch('dishes', queryset=dishes_qs))
            .order_by('order', 'id')
        )
        attach_responsive_image_sources(categories)

        return render(request, 'menu/index.html', {
            'categories': categories,
            'restaurant_info': RestaurantInfo.get_instance(),
            'social_links': SocialLinks.get_instance(),
        })
