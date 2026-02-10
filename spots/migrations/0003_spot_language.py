

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0002_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='language',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
