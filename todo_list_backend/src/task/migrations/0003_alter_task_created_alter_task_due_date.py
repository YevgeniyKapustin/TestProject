# Generated by Django 5.1.1 on 2024-09-16 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_alter_task_created_alter_task_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateTimeField(default='2024-09-16 11:35'),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default='2024-09-16 11:35', verbose_name='Дата завершения задачи'),
        ),
    ]
