

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0007_remove_spot_time_axis_spot_end_at_spot_start_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spot',
            name='image_url',
        ),
        migrations.AddField(
            model_name='spot',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='spots/'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='spot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='spots.spot'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]
