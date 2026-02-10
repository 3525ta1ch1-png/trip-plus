

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0014_alter_spot_parking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spot',
            name='category',
        ),
    ]
