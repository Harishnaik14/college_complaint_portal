from django.db import models


class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('Facilities', 'Facilities'),
        ('Faculty', 'Faculty'),
        ('Hostel', 'Hostel'),
        ('Library', 'Library'),
        ('Transport', 'Transport'),
        ('Canteen', 'Canteen'),
        ('Academics', 'Academics'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    name = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    anonymous = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} ({self.status})"

    @property
    def display_name(self):
        if self.anonymous:
            return 'Anonymous'
        return self.name or 'Unknown'


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

