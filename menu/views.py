from django.db.models import Count, Prefetch, Q
from django.views.generic import TemplateView, View
from django.shortcuts import render

from .models import Category, Dish, Ingredient, RestaurantInfo, Greeting, InfoRule, Fine


class InfoView(TemplateView):
    """Стартовая страница — ознакомление с рестораном."""
    template_name = 'menu/info.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['restaurant_info'] = RestaurantInfo.get_instance()
        ctx['greetings'] = Greeting.objects.all()
        ctx['rules'] = InfoRule.objects.all()
        ctx['fines'] = Fine.objects.all()
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

        categories = (
            Category.objects
            .annotate(dish_count=Count('dishes', filter=Q(dishes__is_available=True)))
            .filter(dish_count__gt=0)
            .prefetch_related(Prefetch('dishes', queryset=dishes_qs))
            .order_by('order', 'id')
        )

        return render(request, 'menu/index.html', {
            'categories': categories,
            'restaurant_info': RestaurantInfo.get_instance(),
        })
