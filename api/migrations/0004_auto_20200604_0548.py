# Generated by Django 3.0.5 on 2020-06-04 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200530_0933'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='precedent',
            unique_together={('precedent', 'participant')},
        ),
    ]