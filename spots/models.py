from django.conf import settings
from django.db import models
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

class Spot(models.Model):

    BUSINESS_DAY_CHOICES = [
        ("mon", "月曜"),
        ("tue", "火曜"),
        ("wed", "水曜"),
        ("thu", "木曜"),
        ("fri", "金曜"),
        ("sat", "土曜"),
        ("sun", "日曜"),
        ("holiday", "年中無休"),
        ("irregular", "不定休"),
    ]

    PARKING_CHOICES = [
        ("有", "有"),
        ("無", "無"),
        ("不明", "不明"),
        ("注意", "注意（公式HP参照）"),
    ]
    parking = models.CharField("駐車場", max_length=20, choices=PARKING_CHOICES, blank=True)
     
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)

    image = models.ImageField(upload_to="spots/", blank=True, null=True)

    website = models.URLField("参考サイト", blank=True)
    phone = models.CharField("電話番号", max_length=30, blank=True)

    business_days = models.JSONField(default=list, blank=True, null=True)
    
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    access = models.CharField(max_length=200, blank=True)

    language = models.CharField("ワード", max_length=30, blank=True)
    mood = models.CharField(max_length=30, blank=True)
    purpose = models.CharField(max_length=30, blank=True)
    time_axis = models.CharField("時間軸", max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        # 住所がある & 座標が未登録のときだけ取得
        if self.address and (self.latitude is None or self.longitude is None):
            geolocator = Nominatim(user_agent="trip-plus")
            geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

            loc = geocode(self.address)
            if loc:
                # DecimalFieldに入れるので float -> str で安全に
                self.latitude = str(loc.latitude)
                self.longitude = str(loc.longitude)

        super().save(*args, **kwargs)

    
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

