# Generated by Django 3.1 on 2024-01-18 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ConerstoneLimmited', '0004_auto_20231219_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='inspection_result',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('F', 'Failed')], max_length=255),
        ),
        migrations.AlterField(
            model_name='transport',
            name='transport_id',
            field=models.CharField(editable=False, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='transport_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('OnTransit', 'Transit'), ('Delivered', 'Delivered')], max_length=20),
        ),
    ]
