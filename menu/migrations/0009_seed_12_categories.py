from django.db import migrations

CATEGORIES = [
    {
        'name': 'Холодные закуски', 'name_en': 'Cold Starters', 'name_ky': 'Суук тамактар',
        'slug': 'cold-starters', 'order': 1,
        'icon_svg': '<path d="M12 2C8 2 4 5 4 9c0 5 8 13 8 13s8-8 8-13c0-4-4-7-8-7z"/>',
        'dishes': [
            {
                'name': 'Карпаччо из говядины', 'name_en': 'Beef Carpaccio', 'name_ky': 'Уй эти карпаччо',
                'slug': 'cold-beef-carpaccio',
                'description': 'Тонко нарезанная говядина с каперсами и пармезаном',
                'description_en': 'Thinly sliced beef with capers and parmesan',
                'description_ky': 'Каперс жана пармезан менен жука кесилген уй эти',
                'price': 650, 'order': 1,
            },
            {
                'name': 'Тартар из лосося', 'name_en': 'Salmon Tartar', 'name_ky': 'Лосось тартары',
                'slug': 'cold-salmon-tartar',
                'description': 'Свежий лосось с авокадо и лимонной заправкой',
                'description_en': 'Fresh salmon with avocado and lemon dressing',
                'description_ky': 'Авокадо жана лимон соусу менен жаңы лосось',
                'price': 720, 'order': 2,
            },
        ],
    },
    {
        'name': 'Горячие закуски', 'name_en': 'Hot Starters', 'name_ky': 'Ысык тамактар',
        'slug': 'hot-starters', 'order': 2,
        'icon_svg': '<path d="M12 2a7 7 0 0 0-7 7c0 4 7 13 7 13s7-9 7-13a7 7 0 0 0-7-7z"/><circle cx="12" cy="9" r="2.5"/>',
        'dishes': [
            {
                'name': 'Жареные креветки', 'name_en': 'Fried Shrimps', 'name_ky': 'Куурулган креветкалар',
                'slug': 'hot-fried-shrimps',
                'description': 'Тигровые креветки в чесночно-сливочном соусе',
                'description_en': 'Tiger shrimps in garlic cream sauce',
                'description_ky': 'Саримсак-каймак соусунда каплан креветкалары',
                'price': 890, 'order': 1,
            },
            {
                'name': 'Брускетта с томатами', 'name_en': 'Bruschetta with Tomatoes', 'name_ky': 'Помидор менен брускетта',
                'slug': 'hot-bruschetta-tomato',
                'description': 'Хрустящий хлеб с томатами черри и базиликом',
                'description_en': 'Crispy bread with cherry tomatoes and basil',
                'description_ky': 'Черри помидор жана базилик менен кытырак нан',
                'price': 420, 'order': 2,
            },
        ],
    },
    {
        'name': 'Супы', 'name_en': 'Soups', 'name_ky': 'Шорполор',
        'slug': 'soups', 'order': 3,
        'icon_svg': '<path d="M4 11h16v2a8 8 0 0 1-16 0v-2z"/><path d="M12 3v4M8 5l1.5 2M16 5l-1.5 2"/>',
        'dishes': [
            {
                'name': 'Крем-суп из тыквы', 'name_en': 'Pumpkin Cream Soup', 'name_ky': 'Асказандын кремсупу',
                'slug': 'soup-pumpkin-cream',
                'description': 'Нежный крем-суп из тыквы с имбирём и сливками',
                'description_en': 'Smooth pumpkin cream soup with ginger and cream',
                'description_ky': 'Имбирь жана каймак менен жумшак асказан кремсупу',
                'price': 480, 'order': 1,
            },
            {
                'name': 'Буйабес', 'name_en': 'Bouillabaisse', 'name_ky': 'Буйабес',
                'slug': 'soup-bouillabaisse',
                'description': 'Французский рыбный суп с морепродуктами и шафраном',
                'description_en': 'French fish soup with seafood and saffron',
                'description_ky': 'Деңиз азыктары жана шафран менен французча балык шорпосу',
                'price': 950, 'order': 2,
            },
        ],
    },
    {
        'name': 'Салаты', 'name_en': 'Salads', 'name_ky': 'Салаттар',
        'slug': 'salads', 'order': 4,
        'icon_svg': '<path d="M12 2C6 2 2 7 2 12s4 10 10 10 10-4 10-10S18 2 12 2z"/><path d="M8 12c0-2.2 1.8-4 4-4s4 1.8 4 4"/>',
        'dishes': [
            {
                'name': 'Цезарь с курицей', 'name_en': 'Caesar with Chicken', 'name_ky': 'Тоок менен Цезарь',
                'slug': 'salad-caesar-chicken',
                'description': 'Классический цезарь с грилованной курицей и анчоусами',
                'description_en': 'Classic Caesar with grilled chicken and anchovies',
                'description_ky': 'Гриль тоок жана анчоус менен классикалык Цезарь',
                'price': 550, 'order': 1,
            },
            {
                'name': 'Салат Нисуаз', 'name_en': 'Nicoise Salad', 'name_ky': 'Нисуаз салаты',
                'slug': 'salad-nicoise',
                'description': 'Тунец, яйца, оливки, стручковая фасоль и помидоры',
                'description_en': 'Tuna, eggs, olives, green beans and tomatoes',
                'description_ky': 'Тунец, жумуртка, зайтун, буурчак жана помидор',
                'price': 620, 'order': 2,
            },
        ],
    },
    {
        'name': 'Основные блюда', 'name_en': 'Main Course', 'name_ky': 'Негизги тамактар',
        'slug': 'mains', 'order': 5,
        'icon_svg': '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
        'dishes': [
            {
                'name': 'Рибай стейк', 'name_en': 'Ribeye Steak', 'name_ky': 'Рибай стейк',
                'slug': 'main-ribeye-steak',
                'description': 'Мраморная говядина гриль с соусом демигляс и овощами',
                'description_en': 'Grilled marbled beef with demi-glace sauce and vegetables',
                'description_ky': 'Демигляс соусу жана жашылчалар менен гриль мрамор уй эти',
                'price': 1800, 'order': 1,
            },
            {
                'name': 'Утиная грудка', 'name_en': 'Duck Breast', 'name_ky': 'Өрдөктүн төшкөй эти',
                'slug': 'main-duck-breast',
                'description': 'Утиная грудка с апельсиновым соусом и картофельным пюре',
                'description_en': 'Duck breast with orange sauce and mashed potatoes',
                'description_ky': 'Апельсин соусу жана картошка пюреси менен өрдөктүн төшкөй эти',
                'price': 1350, 'order': 2,
            },
        ],
    },
    {
        'name': 'Рыба и морепродукты', 'name_en': 'Fish & Seafood', 'name_ky': 'Балык жана деңиз азыктары',
        'slug': 'fish', 'order': 6,
        'icon_svg': '<path d="M2 12s4-8 10-8 10 8 10 8-4 8-10 8S2 12 2 12z"/><circle cx="16" cy="12" r="1.5"/>',
        'dishes': [
            {
                'name': 'Дорадо на гриле', 'name_en': 'Grilled Dorado', 'name_ky': 'Гриль дорадо',
                'slug': 'fish-grilled-dorado',
                'description': 'Целая дорадо с лимоном, каперсами и свежими травами',
                'description_en': 'Whole dorado with lemon, capers and fresh herbs',
                'description_ky': 'Лимон, каперс жана жаңы чөптөр менен бүтүн дорадо',
                'price': 1250, 'order': 1,
            },
            {
                'name': 'Ризотто с морепродуктами', 'name_en': 'Seafood Risotto', 'name_ky': 'Деңиз азыктары менен ризотто',
                'slug': 'fish-seafood-risotto',
                'description': 'Сливочное ризотто с кальмарами, мидиями и креветками',
                'description_en': 'Creamy risotto with squid, mussels and shrimps',
                'description_ky': 'Кальмар, мидия жана креветка менен кремдүү ризотто',
                'price': 1100, 'order': 2,
            },
        ],
    },
    {
        'name': 'Птица', 'name_en': 'Poultry', 'name_ky': 'Куштун эти',
        'slug': 'poultry', 'order': 7,
        'icon_svg': '<path d="M12 4c-1.5 0-3 .5-4 1.5L4 9l2 2 2-2 1 3H7l-2 4h10l-2-4h-2l1-3 2 2 2-2-4-3.5C13.5 4.5 12.8 4 12 4z"/>',
        'dishes': [
            {
                'name': 'Куриное филе с трюфелем', 'name_en': 'Chicken Fillet with Truffle', 'name_ky': 'Трюфель менен тоок филеси',
                'slug': 'poultry-chicken-truffle',
                'description': 'Сочное куриное филе с трюфельным маслом и спаржей',
                'description_en': 'Juicy chicken fillet with truffle butter and asparagus',
                'description_ky': 'Трюфель майы жана кырк уруктуу менен ширелүү тоок филеси',
                'price': 980, 'order': 1,
            },
            {
                'name': 'Перепёлка гриль', 'name_en': 'Grilled Quail', 'name_ky': 'Гриль бөдөнө',
                'slug': 'poultry-grilled-quail',
                'description': 'Запечённая перепёлка с соусом из граната и рукколой',
                'description_en': 'Baked quail with pomegranate sauce and arugula',
                'description_ky': 'Анар соусу жана аругула менен бышырылган бөдөнө',
                'price': 1150, 'order': 2,
            },
        ],
    },
    {
        'name': 'Мясо', 'name_en': 'Meat', 'name_ky': 'Эт тамактар',
        'slug': 'meat', 'order': 8,
        'icon_svg': '<path d="M18.5 3.5L15 7l-3-3-6 6 3 3-4.5 4.5 3.5 3.5L12.5 17l3 3 6-6-3-3 3.5-3.5z"/>',
        'dishes': [
            {
                'name': 'Каре ягнёнка', 'name_en': 'Rack of Lamb', 'name_ky': 'Козу кабырга',
                'slug': 'meat-rack-lamb',
                'description': 'Рёбрышки ягнёнка с розмариновым соусом и картофелем дофинуа',
                'description_en': 'Lamb ribs with rosemary sauce and potatoes dauphinois',
                'description_ky': 'Розмарин соусу жана дофинуа картошкасы менен козу кабырга',
                'price': 1650, 'order': 1,
            },
            {
                'name': 'Телячьи щёчки', 'name_en': 'Veal Cheeks', 'name_ky': 'Бузоо жаак эти',
                'slug': 'meat-veal-cheeks',
                'description': 'Тушёные телячьи щёчки с полентой и трюфельным маслом',
                'description_en': 'Braised veal cheeks with polenta and truffle oil',
                'description_ky': 'Полента жана трюфель майы менен бышырылган бузоо жаак эти',
                'price': 1420, 'order': 2,
            },
        ],
    },
    {
        'name': 'Паста и ризотто', 'name_en': 'Pasta & Risotto', 'name_ky': 'Паста жана ризотто',
        'slug': 'pasta', 'order': 9,
        'icon_svg': '<path d="M4 6h16M4 10h16M4 14h16M4 18h16"/>',
        'dishes': [
            {
                'name': 'Тальятелле с трюфелем', 'name_en': 'Tagliatelle with Truffle', 'name_ky': 'Трюфель менен тальятелле',
                'slug': 'pasta-tagliatelle-truffle',
                'description': 'Свежая паста с трюфельным соусом, пармезаном и яичным желтком',
                'description_en': 'Fresh pasta with truffle sauce, parmesan and egg yolk',
                'description_ky': 'Трюфель соусу, пармезан жана жумуртка сарысы менен жаңы паста',
                'price': 1300, 'order': 1,
            },
            {
                'name': 'Ризотто с грибами', 'name_en': 'Mushroom Risotto', 'name_ky': 'Козу карын менен ризотто',
                'slug': 'pasta-mushroom-risotto',
                'description': 'Сливочное ризотто с белыми грибами и пармезаном',
                'description_en': 'Creamy risotto with porcini mushrooms and parmesan',
                'description_ky': 'Ак козу карын жана пармезан менен кремдүү ризотто',
                'price': 980, 'order': 2,
            },
        ],
    },
    {
        'name': 'Гарниры', 'name_en': 'Side Dishes', 'name_ky': 'Гарнирлер',
        'slug': 'sides', 'order': 10,
        'icon_svg': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>',
        'dishes': [
            {
                'name': 'Картофель дофинуа', 'name_en': 'Potatoes Dauphinois', 'name_ky': 'Дофинуа картошкасы',
                'slug': 'side-potatoes-dauphinois',
                'description': 'Слоёный картофель, запечённый в сливках с чесноком',
                'description_en': 'Layered potatoes baked in cream with garlic',
                'description_ky': 'Саримсак менен каймакта бышырылган катмарлуу картошка',
                'price': 350, 'order': 1,
            },
            {
                'name': 'Спаржа на гриле', 'name_en': 'Grilled Asparagus', 'name_ky': 'Гриль кырк уруктуу',
                'slug': 'side-grilled-asparagus',
                'description': 'Зелёная спаржа с лимонным маслом и морской солью',
                'description_en': 'Green asparagus with lemon butter and sea salt',
                'description_ky': 'Лимон майы жана деңиз тузу менен жашыл кырк уруктуу',
                'price': 320, 'order': 2,
            },
        ],
    },
    {
        'name': 'Десерты', 'name_en': 'Desserts', 'name_ky': 'Таттуулар',
        'slug': 'desserts', 'order': 11,
        'icon_svg': '<path d="M12 2a5 5 0 0 0-5 5v1H5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2h-2V7a5 5 0 0 0-5-5z"/>',
        'dishes': [
            {
                'name': 'Тирамису', 'name_en': 'Tiramisu', 'name_ky': 'Тирамису',
                'slug': 'dessert-tiramisu',
                'description': 'Классический итальянский тирамису с маскарпоне и эспрессо',
                'description_en': 'Classic Italian tiramisu with mascarpone and espresso',
                'description_ky': 'Маскарпоне жана эспрессо менен классикалык италиялык тирамису',
                'price': 480, 'order': 1,
            },
            {
                'name': 'Шоколадный фондан', 'name_en': 'Chocolate Fondant', 'name_ky': 'Шоколад фонданы',
                'slug': 'dessert-chocolate-fondant',
                'description': 'Тёплый шоколадный кекс с жидкой начинкой и ванильным мороженым',
                'description_en': 'Warm chocolate cake with liquid center and vanilla ice cream',
                'description_ky': 'Суюк ортосу жана ваниль балмуздагы менен жылуу шоколад кексу',
                'price': 520, 'order': 2,
            },
        ],
    },
    {
        'name': 'Напитки', 'name_en': 'Drinks', 'name_ky': 'Суусундуктар',
        'slug': 'drinks', 'order': 12,
        'icon_svg': '<path d="M8 2h8l1 7H7L8 2z"/><path d="M7 9c0 5 2 9 5 9s5-4 5-9"/>',
        'dishes': [
            {
                'name': 'Лимонад из базилика', 'name_en': 'Basil Lemonade', 'name_ky': 'Базилик лимонады',
                'slug': 'drink-basil-lemonade',
                'description': 'Свежий лимонад с базиликом, лимоном и мятой',
                'description_en': 'Fresh lemonade with basil, lemon and mint',
                'description_ky': 'Базилик, лимон жана жалбыз менен жаңы лимонад',
                'price': 280, 'order': 1,
            },
            {
                'name': 'Эспрессо', 'name_en': 'Espresso', 'name_ky': 'Эспрессо',
                'slug': 'drink-espresso',
                'description': 'Двойной эспрессо из зерна арабика премиум-класса',
                'description_en': 'Double espresso from premium arabica beans',
                'description_ky': 'Премиум арабика дандынан кош эспрессо',
                'price': 220, 'order': 2,
            },
        ],
    },
]


def seed_forward(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    Dish = apps.get_model('menu', 'Dish')

    for cat_data in CATEGORIES:
        dishes_data = cat_data.pop('dishes')
        cat, _ = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data,
        )
        for dish_data in dishes_data:
            Dish.objects.get_or_create(
                slug=dish_data['slug'],
                defaults={**dish_data, 'category': cat},
            )
        cat_data['dishes'] = dishes_data


def seed_reverse(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    slugs = [c['slug'] for c in CATEGORIES]
    Category.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_add_sociallinks'),
    ]

    operations = [
        migrations.RunPython(seed_forward, seed_reverse),
    ]
