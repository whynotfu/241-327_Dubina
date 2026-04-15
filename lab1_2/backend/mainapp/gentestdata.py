import random
import datetime
from .models import VideoGame
from django.db import transaction
from faker import Faker

fk = Faker()

GENRES = [
    'RPG', 'Action', 'Action RPG', 'Shooter', 'Strategy',
    'Simulation', 'Sports', 'Horror', 'Metroidvania', 'Platformer',
    'Adventure', 'Puzzle', 'Fighting', 'Racing', 'Sandbox',
]


def gentestdata():
    with transaction.atomic():
        for i in range(100):
            release = fk.date_between(
                start_date=datetime.date(1995, 1, 1),
                end_date=datetime.date(2026, 12, 31),
            )
            VideoGame.objects.create(
                title=fk.catch_phrase(),
                genre=random.choice(GENRES),
                release_date=release,
                price=round(random.uniform(0, 3000), 2),
                rating=round(random.uniform(1.0, 10.0), 1),
                is_multiplayer=random.random() > 0.5,
                description=fk.text(max_nb_chars=200),
            )
    print('OK gentestdata() — добавлено 100 записей')
