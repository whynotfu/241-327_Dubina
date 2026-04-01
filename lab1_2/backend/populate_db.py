import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab1.settings')
django.setup()

from lab1_2.backend.mainapp.models import VideoGame
from datetime import date

games = [
    VideoGame(
        title='Elden Ring',
        genre='RPG',
        release_date=date(2022, 2, 25),
        price=1499.99,
        rating=9.5,
        is_multiplayer=True,
        description='Открытый мир от FromSoftware и Джорджа Мартина.',
    ),
    VideoGame(
        title='Cyberpunk 2077',
        genre='Action RPG',
        release_date=date(2020, 12, 10),
        price=999.00,
        rating=8.2,
        is_multiplayer=False,
        description='Футуристический мегаполис Найт-Сити.',
    ),
    VideoGame(
        title='Hollow Knight',
        genre='Metroidvania',
        release_date=date(2017, 2, 24),
        price=349.00,
        rating=9.1,
        is_multiplayer=False,
        description='Инди-платформер в подземном королевстве насекомых.',
    ),
    VideoGame(
        title='Counter-Strike 2',
        genre='Shooter',
        release_date=date(2023, 9, 27),
        price=0.00,
        rating=7.8,
        is_multiplayer=True,
        description='Обновлённый тактический шутер от Valve.',
    ),
    VideoGame(
        title='Red Dead Redemption 2',
        genre='Action-Adventure',
        release_date=date(2018, 10, 26),
        price=1299.00,
        rating=9.7,
        is_multiplayer=True,
        description='Эпическая история о закате эпохи Дикого Запада.',
    ),
]

VideoGame.objects.all().delete()
VideoGame.objects.bulk_create(games)
print(f'Добавлено {len(games)} игр в базу данных.')
