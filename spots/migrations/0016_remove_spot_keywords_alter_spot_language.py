

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0015_remove_spot_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spot',
            name='keywords',
        ),
        migrations.AlterField(
            model_name='spot',
            name='language',
            field=models.CharField(blank=True, max_length=30, verbose_name='ワード'),
        ),
    ]
