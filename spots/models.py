from django.conf import settings
from django.db import models

class Spot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "spot"], name="unique_favorite_user_spot")
        ]

    def __str__(self):
        return f"{self.user} - {self.spot}"

