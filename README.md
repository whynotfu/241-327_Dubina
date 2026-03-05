# Лабораторная работа №1 — Трёхуровневая клиент-серверная архитектура

---

## Цель

Выработка навыков разработки серверного ПО на языках высокого уровня и распространённых фреймворках.

## Задачи

- [ ] Установить необходимый для бэкенд-разработки язык и библиотеки
- [ ] Разработать модель данных
- [ ] Наполнить базу сгенерированными данными
- [ ] Разработать API для доступа к данным (CRUD + List)
- [ ] Продемонстрировать успешный запуск бэкенда на тестовом сервере и запрос к API, предъявить репозиторий Git
- [ ] Защитить теоретическую часть (список вопросов в конце страницы)

---

## Сроки выполнения

| Группа | Срок защиты |
|--------|------------|
| 231-329, 3210 | до **22 марта** |
| 231-3213 | с **26 апреля** по **17 мая** включительно |
| Дедлайн без снижения оценки | **7 июня** |

---

## Порядок выполнения

### 1. Установка Python

Установить версию Python **на 1–2 релиза ниже** текущего последнего.
> Весна 2026 — актуальная версия Python 13, значит устанавливаем **Python 11 или 12**.
![alt text](image.png)
---

### 2. Установка пакетов PyPI

```bash
pip install djangorestframework
pip install psycopg[binary,pool]
pip install faker
pip install gunicorn

# Опционально:
# pip install markdown
# pip install django-filter
# pip install django-cors-headers
```

---

### 3. Создание проекта и приложения Django

```bash
django-admin startproject lab1
cd lab1
django-admin startapp mainapp
```

В файле `settings.py` добавить приложение в `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'mainapp',  # !!!
]
```

> **Задание:** законспектировать (кратко описать) определения, понятия и структуру проекта.

---

### 4. Настройка базы данных

Установить **PostgreSQL** (если уже установлен — переустанавливать не нужно).

Открыть **pgAdmin** или другой инструмент администрирования БД и создать пользователя и базу данных с учётными данными, которые будут прописаны в `settings.py`.

Настройки в `settings.py`:

```python
DATABASES = {
    # SQLite (по умолчанию — отключить):
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }

    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # адаптер для Django ORM + Postgres
        'NAME': 'lab1_db',       # название базы данных
        'USER': 'django',        # пользователь БД (создать вручную)
        'PASSWORD': '2NevjFoQisyVaV',
        'HOST': 'localhost',
        'PORT': 5432,
    },
}
```

---

### 5. Миграции и суперпользователь

```bash
python manage.py makemigrations
python manage.py migrate

# Создать администратора (ввести имя, пароль; email можно пропустить):
python manage.py createsuperuser
```

---

### 6. Модель данных (`models.py`)

Создать модель на основе `django.db.models.Model`, представляющую **реальный объект** (товар, транспортное средство, документ, книга и т.д. — у каждого учащегося модель должна быть **уникальной**).

**Требования:**
- Не менее **5 полей** различных типов

Пример структуры модели (самолёт):

```python
# mainapp/models.py
from django.db import models

class Airplane(models.Model):
    datetime_entry      = models.DateField()
    datetime_withdraw   = models.DateField(null=True, blank=True)
    typename            = models.CharField(max_length=100)
    serial              = models.CharField(max_length=20)
    is_on_maintenance   = models.BooleanField(default=False)
```

---

### 7. Сериализатор (`serializers.py`)

Реализовать сериализатор в JSON на основе `rest_framework.serializers.ModelSerializer`:

```python
# mainapp/serializers.py
from rest_framework import serializers
from .models import Airplane

class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = '__all__'
```

---

### 8. Обработчики запросов (`views.py`)

Реализовать view для пяти основных операций **CRUD + List** на основе `rest_framework.viewsets.ModelViewSet`:

```python
# mainapp/views.py
from rest_framework import viewsets
from .models import Airplane
from .serializers import AirplaneSerializer

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
```

---

### 9. Роутинг (`urls.py`)

```python
# lab1/urls.py
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from mainapp.views import AirplaneViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('airplane',      AirplaneViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('airplane/<pk>', AirplaneViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),
]
```

---

### 10. Заполнение базы тестовыми данными

Создать файл `mainapp/gentestdata.py`:

```python
import random, string, datetime
from .models import Airplane
from django.db import transaction
from faker import Faker

fk = Faker()

def gentestdata():
    with transaction.atomic():
        for i in range(1000):
            plane = Airplane()
            plane.datetime_entry = fk.date_between(
                start_date=datetime.date(2000, 1, 1),
                end_date=datetime.date(2020, 1, 1)
            )
            plane.is_on_maintenance = random.random() > 0.7
            plane.datetime_withdraw = (
                None if plane.is_on_maintenance
                else (fk.date_between(start_date=plane.datetime_entry,
                                      end_date=datetime.datetime.now().date())
                      if random.random() > 0.2 else None)
            )
            plane.typename = random.choice(('Ан-2', 'Ту-134', 'Як-42', 'Другой тип'))
            plane.serial = ''.join(random.sample(string.ascii_letters + string.digits, 5))
            plane.save()
    print('OK gentestdata()')
```

Запуск через Django shell:

```bash
python manage.py shell
```

```python
from mainapp.gentestdata import *
gentestdata()
```

---

## Примеры запросов к REST API

Используйте плагин [REST Client для VS Code](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

```http
@hostname = http://localhost:8000

### Retrieve — получить запись по ID
GET {{hostname}}/airplane/10
Content-Type: application/json

### List — получить все записи
GET {{hostname}}/airplane
Content-Type: application/json

### Create — создать новую запись
POST {{hostname}}/airplane
Content-Type: application/json

{
    "datetime_entry":    "2025-02-15T16:57:59.204261",
    "datetime_withdraw": null,
    "typename":          "newtype",
    "serial":            "newserial",
    "is_on_maintenance": false
}

### TODO: запросы DELETE и PATCH
```

---

## ПО, необходимое для выполнения ЛР

| Инструмент | Версия / Примечание |
|------------|---------------------|
| Python | На 1–2 релиза ниже последнего (весна 2026 → Python 11/12) |
| PostgreSQL | Последняя релизная версия |
| IDE | VS Code (рекомендуется), любая открытая/бесплатная |
| Браузер БД | DBeaver Community |

---

## Порядок проверки практической части

1. Продемонстрировать **незначительное изменение модели данных**, создание и применение миграции в терминале.
2. Продемонстрировать **успешный запуск** бэкенда на встроенном отладочном сервере Django.
3. Продемонстрировать **все 5 запросов** (CRUD + List) из стороннего REST-клиента, вывод в терминале, изменения в данных.
4. Ответить на вопросы по коду, например:
   - _"Покажите строки с настройками соединения бэкенда с базой данных"_
   - _"Покажите, как в исходном коде осуществляется привязка URL и HTTP-метода к функции-обработчику"_

---

## Вопросы для защиты теоретической части

> Для успешной защиты посещайте лекции и лабораторные, изучайте выдаваемые материалы и конспектируйте устные пояснения.

### Термины и аббревиатуры

- **REST** — расшифровка и определение
- **Приложение Django** — что это такое
- **ASGI** / **WSGI** — расшифровка и назначение
- **URL** / **URI** — разница и определения
- **UTC** — расшифровка
- **Транзакция** — определение
- **Миграции баз данных** — назначение и принцип работы

### Назначение и содержимое файлов

| Файл | Назначение |
|------|-----------|
| `manage.py` | ? |
| `settings.py` | ? |
| `urls.py` | ? |
| `models.py` | ? |
| `views.py` | ? |
| `serializers.py` | ? |

### Дополнительные вопросы

1. На каких современных Python-фреймворках имеет смысл начинать бэкенд-проект в 2025 году? (минимум 2) И почему ЛР выполняется именно на Django?

2. **SQLite** (бессерверная БД):
   - Назвать минимум 2 ниши применения
   - Минимум 2 преимущества и 2 недостатка

3. **ORM**:
   - Расшифровка и определение
   - Минимум 2 библиотеки ORM для Python
   - Принцип работы: что происходит при сопоставлении класса ЯП с таблицей SQL
   - Минимум 2 преимущества и 2 недостатка по сравнению с ручными SQL-запросами
   - Минимум 2 наиболее удачные ниши применения ORM
   - Альтернативные подходы к управлению изменениями схемы данных

4. На каких языках и фреймворках имеет смысл начинать **высоконагруженный** проект в 2025 году? (минимум 3 языка и фреймворка)

5. В каком виде в БД следует хранить **пароли пользователей**?

6. Зачем для бэкенда создавать **отдельного пользователя БД** (а не использовать суперпользователя `postgres`)?

7. **Процесс и поток (thread)**: определения и области применения потоков.

---

## Дополнительные задания (бонусные баллы)

<details>
<summary><strong>Барканов — Фоновые задачи и polling (до 15 баллов)</strong></summary>

- `POST /api/task` — запускает фоновую задачу (например, ожидание 20 с + генерация строки/хеша), сразу возвращает `id` задачи
- `GET /api/task?id=<id>` — возвращает статус: `"в процессе"` / `"выполнено"` / `"завершено с ошибкой"` / `"не существует"`
- Поддержка очереди из нескольких задач от нескольких клиентов

**Варианты реализации:**
- Примитивный: `python subprocess` + очередь через БД
- Продвинутый: **Celery** (+5 баллов) + **RabbitMQ/Redis** (+5 баллов)

**Вариант для Коломыченко:** переписать ЛР1 на **Golang** (10 баллов) + доп. задание на Go (15 баллов)

</details>

<details>
<summary><strong>Шкуран / Бардина — OpenAPI + клиент (5 + 20 баллов)</strong></summary>

- Составить **OpenAPI v3**-описание API в формате YAML (5 баллов)
- Отобразить в **Swagger UI** (редактор, плагин VS Code и т.д.)
- Сгенерировать клиентский код на любом языке и продемонстрировать его работу (20 баллов)

</details>

<details>
<summary><strong>Гертнер — Failover proxy для БД (15 баллов)</strong></summary>

- Два контейнера Postgres, у каждого свой том
- Прокси-контейнер между бэкендом и БД
- При отказе одной БД — бэкенд продолжает работать со второй

</details>

<details>
<summary><strong>Гребенников — Система мониторинга (10 баллов)</strong></summary>

Дашборд с отображением:
- Числа HTTP-запросов (по минутам, часам)
- Числа запросов к БД
- Числа установленных HTTP-соединений
- Объёма свободного/занятого места на диске
- Загрузки RAM и CPU

</details>

<details>
<summary><strong>Самохвалов — Авторизация + NGINX (15 баллов)</strong></summary>

- Реализовать `/login` с выдачей API-токена (или JWT)
- Раздача файлов через NGINX только авторизованным пользователям
- NGINX проверяет токен, обращаясь к бэкенду

</details>

<details>
<summary><strong>Тырданов — Golang (20 + 12 баллов)</strong></summary>

- Реализовать ЛР2 на **Go** (20 баллов)
- Реализовать ЛР2 на **gRPC** вместо REST (12 баллов; можно объединить)

</details>

<details>
<summary><strong>Кулибабаев — Исследование QNetworkAccessManager (17 баллов)</strong></summary>

Исследовать поведение Qt при отправке нескольких параллельных запросов до получения ответа на первый:
- Теряются ли запросы на стороне сервера?
- Теряются ли сигналы на стороне клиента?
- В каком порядке приходят ответы?
- Кэширует ли `QNetworkAccessManager` запросы?

Обосновать результаты документацией Qt и фреймворка.

</details>

<details>
<summary><strong>Парц — Загрузка/выгрузка файлов через NGINX (30 баллов)</strong></summary>

- 6 баллов: аутентификация в REST API
- 12 баллов: скачивание файлов — авторизация на бэкенде, выдача через NGINX
- 12 баллов: загрузка файлов — авторизация на бэкенде, загрузка фрагментов через NGINX

**Требования:** файлы в одной папке, без конфликтов имён, оригинальное имя сохраняется при скачивании.

</details>

<details>
<summary><strong>Цой — MinIO + S3 (25 баллов)</strong></summary>

- Развернуть MinIO
- API для загрузки файлов в MinIO
- API для скачивания из S3 — реализовать **прямую загрузку в MinIO** (без «протаскивания» через REST): бэкенд выдаёт одноразовые реквизиты для загрузки напрямую в MinIO

</details>

<details>
<summary><strong>Романов Лев — GraphQL API (20 баллов)</strong></summary>

Реализовать API ЛР1/ЛР2 на **GraphQL**.

</details>

<details>
<summary><strong>Васильев — Prometheus + Grafana (20 баллов)</strong></summary>

- 5 баллов: развернуть Prometheus и Grafana в контейнерах, связать их
- 5 баллов: отображение нагрузки на CPU и объёма памяти
- 5 баллов: число записей в БД — через Prometheus в Grafana
- 5 баллов: число запросов к БД — через Prometheus в Grafana

</details>
