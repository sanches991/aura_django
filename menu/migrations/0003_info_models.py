from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_seed_initial_menu'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_word', models.CharField(default='AURA', max_length=40, verbose_name='Логотип (слово)')),
                ('logo_sub', models.CharField(default='— FINE DINING —', max_length=80, verbose_name='Подпись логотипа')),
                ('page_title', models.CharField(default='Ознакомление', max_length=120, verbose_name='Заголовок страницы')),
                ('hours_open', models.CharField(default='10:00', help_text='Например: 10:00', max_length=10, verbose_name='Время открытия')),
                ('hours_close', models.CharField(default='23:00', help_text='Например: 23:00', max_length=10, verbose_name='Время закрытия')),
            ],
            options={
                'verbose_name': 'Информация о ресторане',
                'verbose_name_plural': 'Информация о ресторане',
            },
        ),
        migrations.CreateModel(
            name='Greeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(help_text='Например: RU, EN, KG', max_length=5, verbose_name='Код языка')),
                ('title', models.CharField(max_length=120, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Приветствие',
                'verbose_name_plural': 'Приветствия',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='InfoRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('icon_svg', models.TextField(blank=True, help_text='Только path/circle внутри <svg>. Сам тег добавляет шаблон.', verbose_name='SVG-иконка (содержимое тега)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Правило',
                'verbose_name_plural': 'Правила',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название штрафа')),
                ('amount', models.PositiveIntegerField(verbose_name='Сумма (сом)')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('icon_svg', models.TextField(blank=True, help_text='Только path/circle внутри <svg>. Сам тег добавляет шаблон.', verbose_name='SVG-иконка (содержимое тега)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Штраф',
                'verbose_name_plural': 'Штрафы',
                'ordering': ['order', 'id'],
            },
        ),
    ]
