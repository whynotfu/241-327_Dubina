# Лабораторная работа №1

## Ход выполнения работы

---

### 1. Установка Python

Установить версию Python **на 1–2 релиза ниже** текущего последнего.

![Установка Python](images/image.png)

---

### 2. Установка пакетов PyPI

| № | Команда |
|---|---------|
| 1 | `pip install djangorestframework` |
| 2 | `pip install psycopg[binary,pool]` |
| 3 | `pip install faker` |
| 4 | `pip install gunicorn` |
| 5 | `pip install django-filter` |
| 6 | `pip install django-cors-headers` |

**1) `pip install djangorestframework`**

![djangorestframework](images/image-1.png)

**2) `pip install psycopg[binary,pool]`**

![psycopg](images/image-2.png)

**3) `pip install faker`** *(уже был установлен)*

![faker](images/image-3.png)

**4) `pip install gunicorn`**

![gunicorn](images/image-4.png)

**5) `pip install django-filter`**

![django-filter](images/image-5.png)

**6) `pip install django-cors-headers`**

![django-cors-headers](images/image-6.png)

---

### 3. Создание проекта и приложения 

![Создание проекта](images/image-7.png)

![Создание приложения](images/image-8.png)

Законспектировать (кратко описать) определения, понятия и структуру проекта.
```
lab1/
├── images/ # изображения для документации lb1.md
│
├── lab1/ # основной конфигурационный пакет 
│ ├── init.py # зависимости 
│ ├── asgi.py # точка входа ASGI (для асинхронных серверов)
│ ├── settings.py # настройки проекта 
│ ├── urls.py # роуты 
│ └── wsgi.py # точка входа WSGI (для веб-серверов)
│
├── mainapp/ # основное приложение 
│ ├── migrations/ # файлы миграций бд
│ ├── init.py # зависимости 
│ ├── admin.py # админ панель
│ ├── apps.py # конфигурация приложения
│ ├── models.py # модели данных (ORM)
│ ├── tests.py # тест кейсы 
│ └── views.py # обработчики HTTP запросов
│
├── lb1.md # отчёт по лабораторной
│
└── manage.py # CLI инструмент управления проектом
```
### Создать скрипты миграции данных и применить их к базе:
![alt text](images/image9.png)

### Создать хотя бы одного пользователя (заодно - администратора).
![alt text](images/image10.png)

![alt text](images/image11.png)