# Generated by Django 5.1.3 on 2025-01-21 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_questionnairesubmission_clicked_stock_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnairesubmission',
            name='distances',
            field=models.TextField(blank=True, null=True),
        ),
    ]
