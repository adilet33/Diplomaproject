# Generated by Django 5.0.6 on 2024-06-18 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application_service', '0004_alter_application_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='resume',
            field=models.FileField(upload_to='resumes/', verbose_name='Резюме'),
        ),
    ]
