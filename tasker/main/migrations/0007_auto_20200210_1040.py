# Generated by Django 3.0.1 on 2020-02-10 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200210_1010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintaskboard',
            name='members',
        ),
        migrations.AddField(
            model_name='advanceduser',
            name='myboard',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.MainTaskBoard'),
        ),
        migrations.AddField(
            model_name='maintaskboard',
            name='creator',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='taskinfo',
            name='t_duration',
            field=models.CharField(choices=[('80', 'Долгосрочные'), ('1', 'Ежедневные'), ('9000', 'Бессрочные'), ('7', 'Еженедельные')], max_length=10, verbose_name='Длительность'),
        ),
    ]
