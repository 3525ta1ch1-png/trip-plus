from django.core.management.base import BaseCommand
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from spots.models import Spot


class Command(BaseCommand):
    help = "住所から緯度経度を取得して Spot に保存する（未登録のみ / 日本向け強化版）"

    def handle(self, *args, **options):
        geolocator = Nominatim(user_agent="trip_plus_geocoder_taichi", timeout=15)

        geocode = RateLimiter(
            geolocator.geocode,
            min_delay_seconds=1,
            max_retries=2,
            error_wait_seconds=3,
            swallow_exceptions=False,
        )

        updated = 0
        skipped = 0

        for s in Spot.objects.all():
            if not s.address:
                skipped += 1
                continue

            if s.latitude and s.longitude:
                skipped += 1
                continue

            queries = [
                f"{s.name} {s.address} 日本",
                f"{s.address} 日本",
                f"{s.name} 日本",
            ]

            loc = None
            last_error = None

            for q in queries:
                try:
                    loc = geocode(
                        q,
                        country_codes="jp",  
                        addressdetails=False,
                        exactly_one=True,
                    )
                    if loc:
                        break
                except (GeocoderTimedOut, GeocoderUnavailable) as e:
                    last_error = e
                    continue

            if not loc:
                if last_error:
                    self.stdout.write(self.style.WARNING(f"取得失敗(通信): {s.name} / {last_error}"))
                else:
                    self.stdout.write(self.style.WARNING(f"見つからない: {s.name} / {s.address}"))
                continue

            s.latitude = loc.latitude
            s.longitude = loc.longitude
            s.save(update_fields=["latitude", "longitude"])
            updated += 1
            self.stdout.write(self.style.SUCCESS(f"更新: {s.name} -> ({s.latitude}, {s.longitude})"))

        self.stdout.write(self.style.SUCCESS(f"完了: 更新 {updated} 件 / スキップ {skipped} 件"))
