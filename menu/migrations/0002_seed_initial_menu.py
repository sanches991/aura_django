"""
Data migration: заполнение БД исходным меню AURA.

После `python manage.py migrate` в базе сразу будут:
    • 4 категории (Салаты / Основные / Десерты / Напитки)
    • 16 блюд (по 4 в каждой категории)
    • Все составы (ингредиенты)

Изображения берутся по URL (поле image_url) — те же Unsplash-снимки,
что были в исходном фронтенде. Через админку их можно заменить
на загруженные файлы (поле image имеет приоритет).
"""
from django.db import migrations


# ============================================================
# КАТЕГОРИИ
# ============================================================
CATEGORIES = [
    {
        'slug': 'salads',
        'name': 'Салаты',
        'order': 1,
        'icon_svg': (
            '<path d="M3 11h18a9 9 0 0 1-18 0Z"/>'
            '<path d="M7 7l1.5-2M12 6V4M16.5 7l1-2"/>'
        ),
    },
    {
        'slug': 'mains',
        'name': 'Основные блюда',
        'order': 2,
        'icon_svg': (
            '<circle cx="12" cy="12" r="9"/>'
            '<circle cx="12" cy="12" r="5"/>'
        ),
    },
    {
        'slug': 'desserts',
        'name': 'Десерты',
        'order': 3,
        'icon_svg': (
            '<path d="M4 13h16l-1.5 7h-13L4 13Z"/>'
            '<path d="M6 13a6 6 0 0 1 12 0"/>'
            '<path d="M12 4v3"/>'
        ),
    },
    {
        'slug': 'drinks',
        'name': 'Напитки',
        'order': 4,
        'icon_svg': (
            '<path d="M6 4h12l-2 9a4 4 0 0 1-4 3 4 4 0 0 1-4-3L6 4Z"/>'
            '<path d="M12 16v4M9 20h6"/>'
        ),
    },
]


# ============================================================
# БЛЮДА (по категориям)
# ============================================================
DISHES = [
    # ---- SALADS ----
    {
        'category_slug': 'salads', 'order': 1,
        'slug': 'salad-avocado',
        'name': 'Салат с авокадо',
        'description': 'Свежие овощи, авокадо, микрозелень и ореховый соус',
        'price': 450,
        'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Авокадо', 'Микрозелень', 'Черри томаты', 'Огурец', 'Ореховый соус', 'Лайм'],
    },
    {
        'category_slug': 'salads', 'order': 2,
        'slug': 'salad-caesar',
        'name': 'Цезарь с курицей',
        'description': 'Листья романо, гренки, пармезан и фирменный соус',
        'price': 520,
        'image_url': 'https://images.unsplash.com/photo-1551248429-40975aa4de74?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Листья романо', 'Куриная грудка', 'Пармезан', 'Гренки', 'Яйцо', 'Соус Цезарь', 'Лимон'],
    },
    {
        'category_slug': 'salads', 'order': 3,
        'slug': 'salad-greek',
        'name': 'Греческий салат',
        'description': 'Томаты, огурцы, фета, оливки и оливковое масло',
        'price': 480,
        'image_url': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Томаты', 'Огурцы', 'Сладкий перец', 'Сыр фета', 'Маслины', 'Оливковое масло', 'Орегано'],
    },
    {
        'category_slug': 'salads', 'order': 4,
        'slug': 'salad-caprese',
        'name': 'Салат Капрезе',
        'description': 'Моцарелла, бычье сердце, базилик и песто',
        'price': 550,
        'image_url': 'https://images.unsplash.com/photo-1608897013039-887f21d8c804?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Моцарелла буффало', 'Томат бычье сердце', 'Базилик', 'Соус песто', 'Оливковое масло', 'Бальзамик'],
    },

    # ---- MAINS ----
    {
        'category_slug': 'mains', 'order': 1,
        'slug': 'main-steak',
        'name': 'Стейк из говядины',
        'description': 'Подаётся с запечёнными овощами и соусом деми-глас',
        'price': 1250,
        'image_url': 'https://images.unsplash.com/photo-1558030006-450675393462?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Говядина рибай 300г', 'Запечённые овощи', 'Молодой картофель', 'Соус деми-глас', 'Розмарин', 'Тимьян'],
    },
    {
        'category_slug': 'mains', 'order': 2,
        'slug': 'main-truffle-pasta',
        'name': 'Паста с трюфелем',
        'description': 'Паста в сливочном соусе с чёрным трюфелем и пармезаном',
        'price': 790,
        'image_url': 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Паста тальятелле', 'Чёрный трюфель', 'Сливки 35%', 'Пармезан', 'Чеснок', 'Сливочное масло'],
    },
    {
        'category_slug': 'mains', 'order': 3,
        'slug': 'main-salmon',
        'name': 'Лосось на гриле',
        'description': 'Филе лосося с овощами гриль и соусом из белого вина',
        'price': 1450,
        'image_url': 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Филе лосося 200г', 'Овощи гриль', 'Соус из белого вина', 'Каперсы', 'Лимон', 'Свежий укроп'],
    },
    {
        'category_slug': 'mains', 'order': 4,
        'slug': 'main-risotto',
        'name': 'Ризотто с грибами',
        'description': 'Сливочное ризотто с белыми грибами и пармезаном',
        'price': 720,
        'image_url': 'https://images.unsplash.com/photo-1476124369491-e7addf5db371?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Рис арборио', 'Белые грибы', 'Пармезан', 'Белое вино', 'Лук-шалот', 'Трюфельное масло'],
    },

    # ---- DESSERTS ----
    {
        'category_slug': 'desserts', 'order': 1,
        'slug': 'dessert-fondant',
        'name': 'Шоколадный фондан',
        'description': 'Тёплый шоколадный кекс с жидкой начинкой',
        'price': 490,
        'image_url': 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Тёмный шоколад 70%', 'Яйца', 'Мука', 'Сливочное масло', 'Сахар', 'Ванильное мороженое'],
    },
    {
        'category_slug': 'desserts', 'order': 2,
        'slug': 'dessert-cheesecake',
        'name': 'Чизкейк с ягодами',
        'description': 'Нежный чизкейк с сезонными ягодами и соусом',
        'price': 450,
        'image_url': 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Сливочный сыр', 'Печенье', 'Сахар', 'Яйца', 'Сезонные ягоды', 'Ягодный соус', 'Сливки'],
    },
    {
        'category_slug': 'desserts', 'order': 3,
        'slug': 'dessert-tiramisu',
        'name': 'Тирамису',
        'description': 'Классический итальянский десерт с маскарпоне и кофе',
        'price': 470,
        'image_url': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Маскарпоне', 'Савоярди', 'Эспрессо', 'Яичные желтки', 'Сахар', 'Какао-порошок'],
    },
    {
        'category_slug': 'desserts', 'order': 4,
        'slug': 'dessert-brulee',
        'name': 'Крем-брюле',
        'description': 'Ванильный крем с карамельной корочкой',
        'price': 440,
        'image_url': 'https://images.unsplash.com/photo-1470124182917-cc6e71b22ecc?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Сливки 35%', 'Яичные желтки', 'Сахар', 'Стручок ванили', 'Карамельная корочка'],
    },

    # ---- DRINKS ----
    {
        'category_slug': 'drinks', 'order': 1,
        'slug': 'drink-lemonade',
        'name': 'Домашний лимонад',
        'description': 'Освежающий лимонад с лимоном, мятой и лаймом',
        'price': 250,
        'image_url': 'https://images.unsplash.com/photo-1621263764928-df1444c5e859?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Лимон', 'Лайм', 'Свежая мята', 'Тростниковый сироп', 'Газированная вода', 'Лёд'],
    },
    {
        'category_slug': 'drinks', 'order': 2,
        'slug': 'drink-mojito',
        'name': 'Мохито б/а',
        'description': 'Освежающий коктейль с мятой, лаймом и содовой',
        'price': 280,
        'image_url': 'https://images.unsplash.com/photo-1541658016709-82535e94bc69?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Лайм', 'Свежая мята', 'Тростниковый сахар', 'Содовая вода', 'Лёд'],
    },
    {
        'category_slug': 'drinks', 'order': 3,
        'slug': 'drink-juice',
        'name': 'Свежевыжатый сок',
        'description': 'Апельсин, яблоко или грейпфрут — на ваш выбор',
        'price': 320,
        'image_url': 'https://images.unsplash.com/photo-1622597467836-f3285f2131b8?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Свежие фрукты', 'Апельсин / Яблоко / Грейпфрут', 'Без добавок'],
    },
    {
        'category_slug': 'drinks', 'order': 4,
        'slug': 'drink-smoothie',
        'name': 'Ягодный смузи',
        'description': 'Клубника, малина, банан и натуральный йогурт',
        'price': 300,
        'image_url': 'https://images.unsplash.com/photo-1553530666-ba11a7da3888?auto=format&fit=crop&w=900&q=80',
        'ingredients': ['Клубника', 'Малина', 'Банан', 'Натуральный йогурт', 'Мёд', 'Лёд'],
    },
]


# ============================================================
# FORWARD: создание записей
# ============================================================
def seed_data(apps, schema_editor):
    Category   = apps.get_model('menu', 'Category')
    Dish       = apps.get_model('menu', 'Dish')
    Ingredient = apps.get_model('menu', 'Ingredient')

    # Категории
    cat_by_slug = {}
    for c in CATEGORIES:
        obj, _ = Category.objects.get_or_create(
            slug=c['slug'],
            defaults={
                'name':     c['name'],
                'order':    c['order'],
                'icon_svg': c['icon_svg'],
            },
        )
        cat_by_slug[c['slug']] = obj

    # Блюда + ингредиенты
    for d in DISHES:
        dish, _ = Dish.objects.get_or_create(
            slug=d['slug'],
            defaults={
                'category':    cat_by_slug[d['category_slug']],
                'name':        d['name'],
                'description': d['description'],
                'price':       d['price'],
                'image_url':   d['image_url'],
                'order':       d['order'],
            },
        )
        for i, name in enumerate(d['ingredients'], start=1):
            Ingredient.objects.get_or_create(
                dish=dish, name=name,
                defaults={'order': i},
            )


# ============================================================
# REVERSE: откат — удаляем всё, что создали
# ============================================================
def unseed_data(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    Category.objects.filter(
        slug__in=[c['slug'] for c in CATEGORIES]
    ).delete()  # CASCADE подчистит блюда и ингредиенты


class Migration(migrations.Migration):
    dependencies = [
        ('menu', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]
