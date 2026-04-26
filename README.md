# AURA — Fine Dining (Django)

Меню ресторана на Django 5.2 + SQLite. Frontend полностью динамический,
все данные тянутся из БД через Django templates. JavaScript отвечает
только за UI-поведение (фильтры, корзина, модалка) и читает данные
из DOM, без хардкода.

## Стек

- **Python 3.10+**
- **Django 5.2 LTS**
- **Pillow** — для работы с `ImageField`
- **SQLite** (для разработки)

## Структура

```
aura_django/
├── manage.py
├── requirements.txt
├── aura_project/          ← настройки проекта
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── menu/                  ← приложение
│   ├── models.py          ← Category, Dish, Ingredient
│   ├── views.py           ← menu_view, info_view
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│       ├── 0001_initial.py
│       └── 0002_seed_initial_menu.py   ← наполнение БД
├── templates/menu/
│   ├── index.html         ← главная (с {% for %})
│   └── info.html
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── images/
└── media/                 ← загружаемые картинки (через админку)
```

## Запуск с нуля

```bash
# 1. Виртуальное окружение
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Зависимости
pip install -r requirements.txt

# 3. Применить миграции (создаст БД + наполнит её 4 категориями
#    и 16 блюдами — теми же, что были в исходном фронтенде)
python manage.py migrate

# 4. Создать суперпользователя для админки
python manage.py createsuperuser

# 5. Запустить
python manage.py runserver
```

После запуска:

- http://127.0.0.1:8000/        — меню
- http://127.0.0.1:8000/info/   — страница «Ознакомление»
- http://127.0.0.1:8000/admin/  — админ-панель

## Модели

### Category
| Поле       | Тип               | Описание                                      |
|------------|-------------------|-----------------------------------------------|
| name       | CharField         | Название («Салаты»)                           |
| slug       | SlugField unique  | Используется в `data-category` (например `salads`) |
| icon_svg   | TextField         | Содержимое тега `<svg>` (только path/circle)  |
| image      | ImageField        | Опциональная картинка категории               |
| order      | PositiveIntegerField | Порядок отображения                        |

### Dish
| Поле         | Тип               | Описание                          |
|--------------|-------------------|-----------------------------------|
| category     | ForeignKey        | → Category, `related_name='dishes'` |
| name         | CharField         | Название блюда                    |
| slug         | SlugField unique  | Используется в `data-id`           |
| description  | TextField         | Короткое описание                  |
| price        | PositiveIntegerField | Цена в сомах                    |
| image        | ImageField        | Загружаемое фото (приоритет)       |
| image_url    | URLField          | Резерв — внешний URL               |
| order        | PositiveIntegerField | Порядок в категории            |
| is_available | BooleanField      | Скрытие из меню без удаления       |

### Ingredient
| Поле  | Тип               | Описание                              |
|-------|-------------------|---------------------------------------|
| dish  | ForeignKey        | → Dish, `related_name='ingredients'`  |
| name  | CharField         | Название ингредиента                  |
| order | PositiveIntegerField | Порядок в списке                   |

## Админка

- **Категории** — список с количеством блюд и редактированием порядка прямо
  из таблицы.
- **Блюда** — фильтр по категории, превью картинки в списке, редактирование
  цены и доступности inline. На странице блюда — встроенное редактирование
  его ингредиентов (TabularInline).
- **Ингредиенты** не имеют отдельной страницы — они редактируются только
  через inline на странице блюда.

## Изображения

В шаблоне:

```django
{% if dish.image %}
  <img src="{{ dish.image.url }}" alt="{{ dish.name }}">
{% else %}
  <img src="{{ dish.image_url }}" alt="{{ dish.name }}">
{% endif %}
```

Если в админке загружен файл — он используется. Иначе — внешний URL
(в seed-миграции это Unsplash-снимки исходного дизайна).

## Полезные команды

```bash
# Создать миграции после изменения моделей
python manage.py makemigrations

# Применить
python manage.py migrate

# Сбросить базу и пересоздать
rm db.sqlite3
python manage.py migrate

# Собрать статику для продакшна
python manage.py collectstatic
```
