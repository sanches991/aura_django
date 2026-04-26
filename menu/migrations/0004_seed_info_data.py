from django.db import migrations


def seed_info(apps, schema_editor):
    RestaurantInfo = apps.get_model('menu', 'RestaurantInfo')
    Greeting = apps.get_model('menu', 'Greeting')
    InfoRule = apps.get_model('menu', 'InfoRule')
    Fine = apps.get_model('menu', 'Fine')

    # --- RestaurantInfo (singleton pk=1) ---
    RestaurantInfo.objects.create(
        pk=1,
        logo_word='AURA',
        logo_sub='— FINE DINING —',
        page_title='Ознакомление',
        hours_open='10:00',
        hours_close='23:00',
    )

    # --- Greetings ---
    Greeting.objects.bulk_create([
        Greeting(
            lang_code='RU', order=1,
            title='Добро пожаловать',
            text=(
                'Рады приветствовать вас в ресторане AURA. Наши повара ежедневно '
                'создают блюда из свежайших продуктов. Мы стремимся сделать каждый '
                'визит незабываемым.'
            ),
        ),
        Greeting(
            lang_code='EN', order=2,
            title='Welcome',
            text=(
                'We are delighted to welcome you to AURA Fine Dining. Our chefs craft '
                'each dish daily from the freshest ingredients. We strive to make every '
                'visit unforgettable.'
            ),
        ),
        Greeting(
            lang_code='KG', order=3,
            title='Кош келиңиз',
            text=(
                'AURA ресторанына кош келиңиз. Биздин ашпозчулар ар күнү эң свежий '
                'продуктулардан тамак даярдашат. Ар бир келүүңүздү унутулгус кылууга '
                'аракет кылабыз.'
            ),
        ),
    ])

    # --- InfoRules ---
    InfoRule.objects.bulk_create([
        InfoRule(
            order=1,
            title='Аллергия',
            description=(
                'Пожалуйста, сообщите персоналу о пищевой аллергии перед заказом. '
                'Мы принимаем все меры предосторожности.'
            ),
            icon_svg=(
                '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3Z"/>'
                '<path d="M9 12l2 2 4-4"/>'
            ),
        ),
        InfoRule(
            order=2,
            title='Время ожидания',
            description=(
                'Большинство блюд готовится 15–30 минут. '
                'В часы пик возможно увеличение до 40 минут.'
            ),
            icon_svg=(
                '<circle cx="12" cy="12" r="9"/>'
                '<path d="M12 7v5l3 2"/>'
            ),
        ),
        InfoRule(
            order=3,
            title='Свежие продукты',
            description=(
                'Все блюда готовятся на заказ. '
                'Меню меняется в зависимости от сезонных продуктов.'
            ),
            icon_svg=(
                '<path d="M3 11h18a9 9 0 0 1-18 0Z"/>'
                '<path d="M7 7l1.5-2M12 6V4M16.5 7l1-2"/>'
            ),
        ),
        InfoRule(
            order=4,
            title='Напитки',
            description=(
                'Наш бар предлагает авторские безалкогольные коктейли, '
                'свежевыжатые соки и горячие напитки.'
            ),
            icon_svg=(
                '<path d="M6 4h12l-2 9a4 4 0 0 1-4 3 4 4 0 0 1-4-3L6 4Z"/>'
                '<path d="M12 16v4M9 20h6"/>'
            ),
        ),
        InfoRule(
            order=5,
            title='Бронирование',
            description=(
                'Для бронирования столика свяжитесь с нами заранее. '
                'Принимаем заявки для банкетов и торжеств.'
            ),
            icon_svg=(
                '<rect x="3" y="4" width="18" height="17" rx="2"/>'
                '<path d="M16 2v4M8 2v4M3 10h18"/>'
            ),
        ),
    ])

    # --- Fines ---
    Fine.objects.bulk_create([
        Fine(
            order=1,
            name='Разбитый бокал',
            amount=500,
            description='Штраф взимается при случайном или намеренном разбитии бокала.',
            icon_svg=(
                '<path d="M8 21h8m-4-6v6"/>'
                '<path d="M4 3h16l-2 8a6 6 0 0 1-12 0L4 3Z"/>'
            ),
        ),
        Fine(
            order=2,
            name='Разбитая тарелка',
            amount=800,
            description='Штраф взимается при разбитии тарелки или другой посуды.',
            icon_svg=(
                '<circle cx="12" cy="12" r="9"/>'
                '<path d="M4.93 4.93l14.14 14.14"/>'
            ),
        ),
        Fine(
            order=3,
            name='Порча имущества ресторана',
            amount=2000,
            description='Повреждение мебели, декора или другого имущества ресторана.',
            icon_svg=(
                '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16'
                'a2 2 0 0 0 1.73-3Z"/>'
                '<path d="M12 9v4m0 4h.01"/>'
            ),
        ),
        Fine(
            order=4,
            name='Нарушение тишины и порядка',
            amount=300,
            description=(
                'Нарушение спокойствия других гостей: громкие крики, '
                'неприличное поведение.'
            ),
            icon_svg=(
                '<path d="M11 5 6 9H2v6h4l5 4V5Z"/>'
                '<path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>'
                '<path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>'
            ),
        ),
    ])


def reverse_seed(apps, schema_editor):
    for model_name in ('RestaurantInfo', 'Greeting', 'InfoRule', 'Fine'):
        apps.get_model('menu', model_name).objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_info_models'),
    ]

    operations = [
        migrations.RunPython(seed_info, reverse_code=reverse_seed),
    ]
