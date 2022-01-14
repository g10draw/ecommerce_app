# Generated by Django 4.0.1 on 2022-01-13 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Created', 'Created'), ('Processing', 'Processing'), ('Completed', 'Completed'), ('Payment Failed', 'Payment Failed')], default='Order Created', max_length=20),
        ),
    ]
