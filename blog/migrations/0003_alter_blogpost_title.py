# Generated by Django 4.0.3 on 2022-05-05 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_chead0_blogpost_chead1_blogpost_chead2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]
