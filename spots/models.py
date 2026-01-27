from django.conf import settings
from django.db import models

class Spot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="spots/", blank=True, null=True)
    language = models.CharField(max_length=30, blank=True)
    mood = models.CharField(max_length=30, blank=True)
    purpose = models.CharField(max_length=30, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.spot} - {self.user} ({self.rating})" 

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "spot"], name="unique_favorite_user_spot")
        ]

    def __str__(self):
        return f"{self.user} - {self.spot}"

