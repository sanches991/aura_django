from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_add_translation_fields'),
    ]

    operations = [
        # RestaurantInfo — page_title translations
        migrations.AddField(
            model_name='restaurantinfo',
            name='page_title_en',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='Заголовок страницы (EN)'),
        ),
        migrations.AddField(
            model_name='restaurantinfo',
            name='page_title_ky',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='Заголовок страницы (KY)'),
        ),

        # InfoRule — title & description translations
        migrations.AddField(
            model_name='inforule',
            name='title_en',
            field=models.CharField(blank=True, max_length=120, verbose_name='Заголовок (EN)'),
        ),
        migrations.AddField(
            model_name='inforule',
            name='title_ky',
            field=models.CharField(blank=True, max_length=120, verbose_name='Заголовок (KY)'),
        ),
        migrations.AddField(
            model_name='inforule',
            name='description_en',
            field=models.TextField(blank=True, verbose_name='Описание (EN)'),
        ),
        migrations.AddField(
            model_name='inforule',
            name='description_ky',
            field=models.TextField(blank=True, verbose_name='Описание (KY)'),
        ),

        # Fine — name & description translations
        migrations.AddField(
            model_name='fine',
            name='name_en',
            field=models.CharField(blank=True, max_length=120, verbose_name='Название (EN)'),
        ),
        migrations.AddField(
            model_name='fine',
            name='name_ky',
            field=models.CharField(blank=True, max_length=120, verbose_name='Название (KY)'),
        ),
        migrations.AddField(
            model_name='fine',
            name='description_en',
            field=models.TextField(blank=True, verbose_name='Описание (EN)'),
        ),
        migrations.AddField(
            model_name='fine',
            name='description_ky',
            field=models.TextField(blank=True, verbose_name='Описание (KY)'),
        ),
    ]
