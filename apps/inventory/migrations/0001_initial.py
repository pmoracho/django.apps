# Generated by Django 2.0.5 on 2018-05-19 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aplicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('atajo', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Aplicaciones',
                'verbose_name': 'Aplicacion',
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Areas',
                'verbose_name': 'Area',
            },
        ),
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Entidades',
                'verbose_name': 'Entidad',
            },
        ),
        migrations.CreateModel(
            name='Funcionalidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=255)),
                ('observacion', models.CharField(blank=True, max_length=1000)),
                ('entrada_usuario', models.CharField(blank=True, max_length=255)),
                ('salida_usuario', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Funcionalidades',
                'verbose_name': 'Funcionalidad',
            },
        ),
        migrations.CreateModel(
            name='FuncionalidadEntidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion', models.CharField(blank=True, max_length=1000)),
                ('entidad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Entidad')),
                ('funcionalidad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Funcionalidad')),
            ],
            options={
                'verbose_name_plural': 'Entidades por funcionalidad',
                'verbose_name': 'Entidad por funcionalidad',
            },
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('grupo', models.CharField(blank=True, max_length=255)),
                ('aplicacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Aplicacion')),
            ],
            options={
                'verbose_name_plural': 'Modulos',
                'verbose_name': 'Modulo',
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Proyectos',
                'verbose_name': 'Proyecto',
            },
        ),
        migrations.CreateModel(
            name='Sistema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Area')),
            ],
            options={
                'verbose_name_plural': 'Sistemas',
                'verbose_name': 'Sistemas',
            },
        ),
        migrations.CreateModel(
            name='TipoEntidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name_plural': 'Tipo de entidades',
                'verbose_name': 'Tipo de entidad',
            },
        ),
        migrations.CreateModel(
            name='TipoFuncionalidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name_plural': 'Tipos de funcionalidades',
                'verbose_name': 'Tipo de funcionalidad',
            },
        ),
        migrations.AddField(
            model_name='funcionalidadentidad',
            name='modo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.TipoFuncionalidad'),
        ),
        migrations.AddField(
            model_name='funcionalidad',
            name='entidades',
            field=models.ManyToManyField(through='inventory.FuncionalidadEntidad', to='inventory.Entidad'),
        ),
        migrations.AddField(
            model_name='funcionalidad',
            name='modulo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Modulo'),
        ),
        migrations.AddField(
            model_name='funcionalidad',
            name='tipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.TipoFuncionalidad'),
        ),
        migrations.AddField(
            model_name='entidad',
            name='origen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Sistema'),
        ),
        migrations.AddField(
            model_name='entidad',
            name='tipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.TipoEntidad'),
        ),
        migrations.AddField(
            model_name='area',
            name='proyecto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Proyecto'),
        ),
        migrations.AddField(
            model_name='aplicacion',
            name='sistema',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Sistema'),
        ),
    ]
