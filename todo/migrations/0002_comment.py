from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=models.CASCADE, related_name='comments', to='todo.task')),
            ],
        ),
    ]
