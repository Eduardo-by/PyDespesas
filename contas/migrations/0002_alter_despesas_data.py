# Generated by Django 4.2.4 on 2023-08-03 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesas',
            name='data',
            field=models.DateField(),
        ),
    ]