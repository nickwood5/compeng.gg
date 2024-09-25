# Generated by Django 5.0.7 on 2024-09-25 00:22

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0009_assignment_runner"),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "offering",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teams",
                        to="courses.offering",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="enrollment",
            name="team",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="members",
                to="courses.team",
            ),
        ),
        migrations.AddConstraint(
            model_name="team",
            constraint=models.UniqueConstraint(
                fields=("name", "offering"), name="unique_team_name_per_offering"
            ),
        ),
    ]