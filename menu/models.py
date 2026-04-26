from django.db import models


# ============================================================
# CATEGORY
# ============================================================
class Category(models.Model):
    """Категория блюд: Салаты, Основные блюда, Десерты, Напитки."""

    name = models.CharField(
        max_length=80,
        verbose_name='Название (RU)',
        help_text='Например: «Салаты», «Десерты»'
    )
    name_en = models.CharField(
        max_length=80, blank=True,
        verbose_name='Название (EN)',
    )
    name_ky = models.CharField(
        max_length=80, blank=True,
        verbose_name='Название (KY)',
    )
    slug = models.SlugField(
        max_length=40,
        unique=True,
        verbose_name='Slug',
        help_text=(
            'Используется в data-category атрибутах HTML и в URL. '
            'Существующие значения: salads, mains, desserts, drinks.'
        ),
    )
    icon_svg = models.TextField(
        blank=True,
        verbose_name='SVG-иконка (внутреннее содержимое)',
        help_text=(
            'Только содержимое тега &lt;svg&gt; (path, circle и т.д.). '
            'Сам тег &lt;svg&gt; добавляется шаблоном.'
        ),
    )
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        verbose_name='Картинка категории (опционально)',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения',
        help_text='Чем меньше, тем выше в списке.',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


# ============================================================
# DISH
# ============================================================
class Dish(models.Model):
    """Блюдо в меню."""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='dishes',        
        verbose_name='Категория',
    )
    name = models.CharField(
        max_length=120,
        verbose_name='Название (RU)',
    )
    name_en = models.CharField(
        max_length=120, blank=True,
        verbose_name='Название (EN)',
    )
    name_ky = models.CharField(
        max_length=120, blank=True,
        verbose_name='Название (KY)',
    )
    slug = models.SlugField(
        max_length=80,
        unique=True,
        verbose_name='Slug',
        help_text=(
            'Используется в data-id атрибутах HTML. '
            'Например: salad-avocado, main-steak.'
        ),
    )
    description = models.TextField(
        verbose_name='Описание (RU)',
        help_text='Короткое описание под названием блюда.',
    )
    description_en = models.TextField(
        blank=True,
        verbose_name='Описание (EN)',
    )
    description_ky = models.TextField(
        blank=True,
        verbose_name='Описание (KY)',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена (сом)',
    )
    image = models.ImageField(
        upload_to='dishes/',
        blank=True,
        null=True,
        verbose_name='Изображение (загружаемое)',
        help_text='Если загружено, имеет приоритет над URL.',
    )
    image_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='URL изображения (резерв)',
        help_text='Используется, если картинка не загружена.',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок в категории',
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Доступно для заказа',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['category__order', 'order', 'id']

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    @property
    def display_image(self):
        """
        Возвращает URL картинки: загруженный файл или внешний URL.
        Используется в шаблоне: {{ dish.display_image }}.
        """
        if self.image:
            return self.image.url
        return self.image_url


# ============================================================
# INGREDIENT
# ============================================================
class Ingredient(models.Model):
    """Ингредиент блюда (отображается в модальном окне состава)."""

    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='ingredients',     
        verbose_name='Блюдо',
    )
    name = models.CharField(
        max_length=120,
        verbose_name='Ингредиент (RU)',
    )
    name_en = models.CharField(
        max_length=120, blank=True,
        verbose_name='Ингредиент (EN)',
    )
    name_ky = models.CharField(
        max_length=120, blank=True,
        verbose_name='Ингредиент (KY)',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


# ============================================================
# RESTAURANT INFO  (синглтон — страница ознакомления)
# ============================================================
class RestaurantInfo(models.Model):
    """Основные реквизиты ресторана для страницы info.html."""

    logo_word = models.CharField(
        max_length=40, default='AURA', verbose_name='Логотип (слово)',
    )
    logo_sub = models.CharField(
        max_length=80, default='— FINE DINING —', verbose_name='Подпись логотипа',
    )
    page_title = models.CharField(
        max_length=120, default='Ознакомление', verbose_name='Заголовок страницы',
    )
    hours_open = models.CharField(
        max_length=10, default='10:00', verbose_name='Время открытия',
        help_text='Например: 10:00',
    )
    hours_close = models.CharField(
        max_length=10, default='23:00', verbose_name='Время закрытия',
        help_text='Например: 23:00',
    )

    class Meta:
        verbose_name = 'Информация о ресторане'
        verbose_name_plural = 'Информация о ресторане'

    def __str__(self):
        return self.logo_word

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            'logo_word': 'AURA',
            'logo_sub': '— FINE DINING —',
            'page_title': 'Ознакомление',
            'hours_open': '10:00',
            'hours_close': '23:00',
        })
        return obj


# ============================================================
# GREETING
# ============================================================
class Greeting(models.Model):
    """Приветствие на разных языках (страница ознакомления)."""

    lang_code = models.CharField(
        max_length=5, verbose_name='Код языка',
        help_text='Например: RU, EN, KG',
    )
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Приветствие'
        verbose_name_plural = 'Приветствия'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.lang_code}: {self.title}'


# ============================================================
# INFO RULE
# ============================================================
class InfoRule(models.Model):
    """Правило / важная информация (страница ознакомления)."""

    title = models.CharField(max_length=120, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    icon_svg = models.TextField(
        blank=True, verbose_name='SVG-иконка (содержимое тега)',
        help_text='Только path/circle внутри &lt;svg&gt;. Сам тег добавляет шаблон.',
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Правило'
        verbose_name_plural = 'Правила'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


# ============================================================
# FINE
# ============================================================
class Fine(models.Model):
    """Штраф за нарушение правил ресторана."""

    name = models.CharField(max_length=120, verbose_name='Название штрафа')
    amount = models.PositiveIntegerField(verbose_name='Сумма (сом)')
    description = models.TextField(blank=True, verbose_name='Описание')
    icon_svg = models.TextField(
        blank=True, verbose_name='SVG-иконка (содержимое тега)',
        help_text='Только path/circle внутри &lt;svg&gt;. Сам тег добавляет шаблон.',
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Штраф'
        verbose_name_plural = 'Штрафы'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.name} — {self.amount} сом'
