# Generated by Django 5.2.2 on 2025-06-12 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_rename_comment_comment_izoh'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CommentLike',
        ),
    ]
