# Generated by Django 2.0.7 on 2018-10-29 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0004_auto_20181017_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticecomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='notice.NoticeComment'),
        ),
    ]
