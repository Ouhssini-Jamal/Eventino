# Generated by Django 4.2.1 on 2023-06-21 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_event_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to='event_images/'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='quantity_left',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
