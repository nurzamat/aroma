# Generated by Django 2.1.5 on 2019-04-04 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_testimonials'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sliders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='Название')),
                ('image', models.ImageField(blank=True, upload_to='news/%Y/%m/%d/', verbose_name='Изображение')),
                ('video', models.URLField(blank=True, verbose_name='Ссылка на видео')),
                ('description', models.TextField(blank=True, verbose_name='Текст')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Слайд',
                'verbose_name_plural': 'Слайдер',
            },
        ),
    ]
