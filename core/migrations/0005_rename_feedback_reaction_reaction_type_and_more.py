# Generated by Django 5.0.2 on 2024-08-22 08:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_product_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reaction',
            old_name='feedback',
            new_name='reaction_type',
        ),
        migrations.AlterField(
            model_name='reaction',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='core.comment'),
        ),
    ]
