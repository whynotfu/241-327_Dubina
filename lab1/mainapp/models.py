from django.db import models

class VideoGame(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    rating = models.FloatField()
    is_multiplayer = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
