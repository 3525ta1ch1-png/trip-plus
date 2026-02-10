

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0011_spot_business_days_spot_business_hours_spot_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spot',
            name='business_hours',
        ),
        migrations.RemoveField(
            model_name='spot',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='spot',
            name='price_range',
        ),
        migrations.AddField(
            model_name='spot',
            name='access',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='spot',
            name='close_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='spot',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='spot',
            name='open_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='spot',
            name='business_days',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
