from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_add_info_translation_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whatsapp_url', models.URLField(blank=True, default='', max_length=600, verbose_name='Ссылка WhatsApp')),
                ('instagram_url', models.URLField(blank=True, default='', verbose_name='Ссылка Instagram')),
                ('telegram_url', models.URLField(blank=True, default='', verbose_name='Ссылка Telegram')),
            ],
            options={
                'verbose_name': 'Социальные сети',
                'verbose_name_plural': 'Социальные сети',
            },
        ),
    ]
