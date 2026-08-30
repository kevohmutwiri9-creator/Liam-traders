from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0004_levelupgradepayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(max_length=50, default='general'),
        ),
    ]
