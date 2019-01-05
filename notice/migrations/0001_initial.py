# Generated by Django 2.0.7 on 2018-10-04 02:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='공지사항 제목을 입력해주세요. 최대 100자 내외.', max_length=100, unique=True)),
                ('content', models.TextField()),
                ('photo', models.ImageField(blank=True, upload_to='notice/photo/%Y/%m/%d')),
                ('option', models.CharField(blank=True, choices=[('f', '고정'), ('n', '일반')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
    ]
