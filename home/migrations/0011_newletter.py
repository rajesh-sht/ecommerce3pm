# Generated by Django 4.1.5 on 2023-02-17 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=300)),
            ],
        ),
    ]