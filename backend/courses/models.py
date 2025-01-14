from django.conf import settings
from django.db import models
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext_lazy as _

from runner.models import Runner, Task

class Institution(models.Model):

    slug = models.SlugField(max_length=50)
    name = models.CharField(max_length=50)
    verified_discord_role_id = models.BigIntegerField(blank=True, null=True)
    first_year_discord_role_id = models.BigIntegerField(blank=True, null=True)
    second_year_discord_role_id = models.BigIntegerField(blank=True, null=True)
    third_year_discord_role_id = models.BigIntegerField(blank=True, null=True)
    fourth_year_discord_role_id = models.BigIntegerField(blank=True, null=True)
    grad_student_discord_role_id = models.BigIntegerField(blank=True, null=True)
    faculty_discord_role_id = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if Offering.objects.filter(course__institution=self,
                                   active=False) \
                           .exists():
            return reverse('courses:archive_institution',
                            kwargs={'institution_slug': self.slug})
        raise NoReverseMatch(f'{self} has no archived offerings')

    class Meta:
        ordering = ['slug']

class Course(models.Model):

    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(max_length=50)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if Offering.objects.filter(course=self, active=False).exists():
            return reverse('courses:archive_course', kwargs={
                'institution_slug': self.institution.slug,
                'course_slug': self.slug,
            })
        raise NoReverseMatch(f'{self} has no archived offerings')

    class Meta:
        ordering = ['slug']

class Offering(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(max_length=50)
    name = models.CharField(max_length=50)
    start = models.DateField()
    end = models.DateField()
    active = models.BooleanField()
    external_id = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.course}'

    def full_slug(self):
        return f'{self.slug}-{self.course.slug}'

    def get_absolute_url(self):
        if self.active:
            return reverse('courses:course', kwargs={'course_slug': self.course.slug})
        else:
            return reverse('courses:archive_offering', kwargs={
                'institution_slug': self.course.institution.slug,
                'course_slug': self.course.slug,
                'offering_slug': self.slug,
            })

    class Meta:
        ordering = ['-start', 'slug']

class Assignment(models.Model):

    offering = models.ForeignKey(
        Offering,
        on_delete=models.CASCADE,
    )
    runner = models.ForeignKey(
        Runner,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    slug = models.SlugField(max_length=50)
    name = models.CharField(max_length=50)
    due_date = models.DateTimeField()
    files = models.JSONField()

    def __str__(self):
        return f'{self.offering} - {self.name}'

    class Meta:
        ordering = ['-due_date']

class Role(models.Model):

    class Kind(models.IntegerChoices):
        INSTRUCTOR = 1, _('Instructor')
        TA = 2, _('TA')
        STUDENT = 3, _('Student')
        AUDIT = 4, _('Audit')

    kind = models.IntegerField(choices=Kind)
    offering = models.ForeignKey(
        Offering,
        on_delete=models.CASCADE,
    )
    discord_role_id = models.BigIntegerField(blank=True, null=True)
    github_team_slug = models.CharField(max_length=128, blank=True, null=False)

    def __str__(self):
        return f'{self.offering} {self.get_kind_display()}'

    class Meta:
        unique_together = ['kind', 'offering']

class Member(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
    )
    external_id = models.BigIntegerField()

    def __str__(self):
        return f'{self.user} ({self.external_id})'

    class Meta:
        unique_together = ['institution', 'external_id']

class Enrollment(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user} - {self.role}'

    class Meta:
        unique_together = ['user', 'role']

class AssignmentTask(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user} - {self.assignment} - {self.task}'
