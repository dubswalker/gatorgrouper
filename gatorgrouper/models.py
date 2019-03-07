""" This is undocumented """
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Professor(AbstractUser):
    """ This is undocumented """
    REQUIRED_FIELDS = ('first_name','last_name')
    USERNAME_FIELD = 'email'
    username = None
    email = models.EmailField(max_length=200, unique=True)
    professor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    if not email:
        raise ValueError('Users must have an email address')
    objects = UserManager()

    def __str__(self):
        return "{}, {}".format(self.last_name, self.first_name)


class Semester_Class(models.Model):
    """ This is undocumented """

    professor_id = models.ForeignKey(Professor, on_delete=models.CASCADE)
    SPRING_2019 = "S19"
    FALL_2019 = "F19"
    SEMESTER_CHOICES = ((SPRING_2019, "Spring, 2019"), (FALL_2019, "Fall, 2019"))
    semester = models.CharField(
        max_length=3, choices=SEMESTER_CHOICES, default="---------"
    )
    class_id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=10)
    class_number = models.CharField(max_length=10)
    class_section = models.CharField(max_length=10)
    domain_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "{}: {}*{}".format(
            self.department, self.class_number, self.class_section
        )


class Assignment(models.Model):
    """ This is undocumented """

    class_id = models.ForeignKey(Semester_Class, on_delete=models.CASCADE)
    assignment_id = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return "{}".format(self.assignment_id)


class Student(models.Model):
    """ This is undocumented """

    class_id = models.ForeignKey(Semester_Class, on_delete=models.CASCADE)
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return "{}, {}".format(self.last_name, self.first_name)


class Grouped_Student(models.Model):
    """ This is undocumented """

    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    group_id = models.CharField(max_length=40)

    def __str__(self):
        return "{}: {}".format(self.assignment_id, self.group_id)