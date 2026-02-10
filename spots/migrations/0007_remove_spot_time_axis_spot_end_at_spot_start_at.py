

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0006_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spot',
            name='time_axis',
        ),
        migrations.AddField(
            model_name='spot',
            name='end_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='spot',
            name='start_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
