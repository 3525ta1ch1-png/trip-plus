

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0003_spot_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='mood',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='spot',
            name='purpose',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='spot',
            name='time_axis',
            field=models.CharField(blank=True, null=True, default='', max_length=30),
            preserve_default=False,
        ),
    ]
