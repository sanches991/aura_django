from django.contrib import admin
from django.utils.html import format_html, mark_safe

from .models import Category, Dish, Ingredient, RestaurantInfo, Greeting, InfoRule, Fine, SocialLinks


_DEFAULT_RULE_ICON = '<circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/>'
_DEFAULT_FINE_ICON = '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4m0 4h.01"/>'
_DEFAULT_CAT_ICON  = '<path d="M4 6h16M4 12h16M4 18h16"/>'


def _svg_badge(icon_svg, bg='#edf6f0', color='#2d5a3d', size=32, icon_size=15):
    """Render an SVG icon inside a rounded badge."""
    return format_html(
        '<span style="display:inline-flex;align-items:center;justify-content:center;'
        'width:{sz}px;height:{sz}px;border-radius:50%;background:{bg};color:{fg};flex-shrink:0">'
        '<svg viewBox="0 0 24 24" width="{isz}" height="{isz}" fill="none" stroke="currentColor"'
        ' stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>'
        '</span>',
        sz=size, bg=bg, fg=color, isz=icon_size,
        inner=mark_safe(icon_svg),
    )


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 2
    fields = ('order', 'name', 'name_en', 'name_ky')
    ordering = ('order',)
    show_change_link = False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display        = ('icon_badge', 'name', 'slug', 'order', 'dish_count')
    list_display_links  = ('icon_badge', 'name')
    list_editable       = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields       = ('name', 'slug')
    ordering            = ('order',)
    save_on_top         = True

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'icon_svg', 'image', 'order'),
        }),
        ('Переводы', {
            'fields': ('name_en', 'name_ky'),
            'classes': ('collapse',),
            'description': 'Заполните для поддержки английского и кыргызского языков.',
        }),
    )

    @admin.display(description='')
    def icon_badge(self, obj):
        return _svg_badge(obj.icon_svg or _DEFAULT_CAT_ICON)

    @admin.display(description='Блюд')
    def dish_count(self, obj):
        count = obj.dishes.count()
        url = f'../dish/?category__id__exact={obj.pk}'
        return format_html('<a href="{}">{} шт.</a>', url, count)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display        = ('image_preview', 'name', 'category', 'price',
                           'is_available', 'order')
    list_display_links  = ('image_preview', 'name')
    list_filter         = ('name', 'category', 'is_available')
    list_editable       = ('price', 'is_available', 'order')
    search_fields       = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines             = [IngredientInline]
    autocomplete_fields = ('category',)
    save_on_top         = True
    list_per_page       = 25
    readonly_fields     = ('image_preview_large', 'created_at', 'updated_at')

    class Media:
        css = {'all': ('admin/css/dish_admin.css',)}

    fieldsets = (
        ('Основное (RU)', {
            'fields': ('name', 'slug', 'category', 'description', 'price'),
        }),
        ('Перевод EN', {
            'fields': ('name_en', 'description_en'),
            'classes': ('collapse',),
        }),
        ('Перевод KY', {
            'fields': ('name_ky', 'description_ky'),
            'classes': ('collapse',),
        }),
        ('Изображение', {
            'fields': ('image', 'image_url', 'image_preview_large'),
            'description': 'Если загружено фото — оно имеет приоритет над URL.',
        }),
        ('Статус и порядок', {
            'fields': ('is_available', 'order'),
        }),
        ('Служебное', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Фото')
    def image_preview(self, obj):
        url = obj.display_image
        if not url:
            return format_html('<span style="color:#888">—</span>')
        return format_html(
            '<img src="{}" style="height:44px;width:44px;object-fit:cover;'
            'border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.4)">',
            url,
        )

    @admin.display(description='Превью изображения')
    def image_preview_large(self, obj):
        url = obj.display_image
        if not url:
            return '—'
        return format_html(
            '<img src="{}" style="max-height:200px;max-width:320px;'
            'object-fit:cover;border-radius:10px;">',
            url,
        )


@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    save_on_top = True

    fieldsets = (
        ('Основное', {
            'fields': ('logo_word', 'logo_sub', 'page_title', 'hours_open', 'hours_close'),
        }),
        ('Переводы заголовка страницы', {
            'fields': ('page_title_en', 'page_title_ky'),
            'classes': ('collapse',),
            'description': 'Заполните для поддержки английского и кыргызского языков.',
        }),
    )

    def has_add_permission(self, request):
        return not RestaurantInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Greeting)
class GreetingAdmin(admin.ModelAdmin):
    list_display  = ('lang_code', 'title', 'order')
    list_editable = ('order',)
    search_fields = ('lang_code', 'title', 'text')
    ordering      = ('order',)
    save_on_top   = True


@admin.register(InfoRule)
class InfoRuleAdmin(admin.ModelAdmin):
    list_display        = ('icon_badge', 'title', 'order')
    list_display_links  = ('icon_badge', 'title')
    list_editable       = ('order',)
    search_fields       = ('title', 'description')
    ordering            = ('order',)
    save_on_top         = True

    @admin.display(description='')
    def icon_badge(self, obj):
        return _svg_badge(obj.icon_svg or _DEFAULT_RULE_ICON)

    fieldsets = (
        ('Основное (RU)', {
            'fields': ('title', 'description', 'icon_svg', 'order'),
        }),
        ('Перевод EN', {
            'fields': ('title_en', 'description_en'),
            'classes': ('collapse',),
        }),
        ('Перевод KY', {
            'fields': ('title_ky', 'description_ky'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display        = ('icon_badge', 'name', 'amount', 'order')
    list_display_links  = ('icon_badge', 'name')
    list_editable       = ('amount', 'order')
    search_fields       = ('name', 'description')
    ordering            = ('order',)
    save_on_top         = True

    @admin.display(description='')
    def icon_badge(self, obj):
        return _svg_badge(obj.icon_svg or _DEFAULT_FINE_ICON,
                          bg='#fef3ec', color='#b85c1e')

    fieldsets = (
        ('Основное (RU)', {
            'fields': ('name', 'amount', 'description', 'icon_svg', 'order'),
        }),
        ('Перевод EN', {
            'fields': ('name_en', 'description_en'),
            'classes': ('collapse',),
        }),
        ('Перевод KY', {
            'fields': ('name_ky', 'description_ky'),
            'classes': ('collapse',),
        }),
    )


@admin.register(SocialLinks)
class SocialLinksAdmin(admin.ModelAdmin):
    save_on_top = True

    fieldsets = (
        ('Ссылки на социальные сети', {
            'fields': ('whatsapp_url', 'instagram_url', 'telegram_url'),
            'description': 'Ссылки отображаются в футере сайта. Оставьте поле пустым, чтобы скрыть иконку.',
        }),
    )

    def has_add_permission(self, _request):
        return not SocialLinks.objects.exists()

    def has_delete_permission(self, _request, _obj=None):
        return False
