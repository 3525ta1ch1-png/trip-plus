

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0013_alter_spot_business_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='parking',
            field=models.CharField(blank=True, choices=[('有', '有'), ('無', '無'), ('不明', '不明'), ('注意', '注意（公式HP参照）')], max_length=20, verbose_name='駐車場'),
        ),
    ]
