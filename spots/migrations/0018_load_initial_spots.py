from django.core.management import call_command
from django.db import migrations


def load_initial_spots(apps, schema_editor):
    Spot = apps.get_model("spots", "Spot")

    # すでにスポットが入っている環境では二重投入しない
    if Spot.objects.exists():
        return

    # spots/fixtures/initial_spots.json を読む
    call_command("loaddata", "initial_spots", verbosity=0)


class Migration(migrations.Migration):

    dependencies = [
        ("spots", "0017_spot_created_by"),  # ← ★ここだけ直す
    ]

    operations = [
        migrations.RunPython(load_initial_spots, migrations.RunPython.noop),
    ]