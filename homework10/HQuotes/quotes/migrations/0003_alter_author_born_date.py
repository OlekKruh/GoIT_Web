# Generated by Django 5.0.3 on 2024-03-16 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0002_author_alter_quote_text_alter_quote_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='born_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
