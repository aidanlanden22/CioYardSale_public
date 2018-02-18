from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    # Using the built-in Django User model for now
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Let the student select a year option
    FIRSTYEAR = 'FIRST'
    SECONDYEAR = 'SECOND'
    THIRDYEAR = 'THIRD'
    FOURTHYEAR = 'FOURTH'
    POSTGRAD = 'POST'
    NONSTUD = 'NON'
    YEAR_IN_SCHOOL_CHOICES = (
        (FIRSTYEAR, 'First Year'),
        (SECONDYEAR, 'Second Year'),
        (THIRDYEAR, 'Third Year'),
        (FOURTHYEAR, 'Fourth Year'),
        (POSTGRAD, 'Post-Grad'),
        (NONSTUD, 'Non-Student'),
    )
    year = models.CharField(
        max_length=6,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FIRSTYEAR,
    )

    
