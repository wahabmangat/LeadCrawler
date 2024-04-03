from django.db import models
from linkedin_scraper.utils import TimeStamped

class ProfileData(TimeStamped):
    first_name = models.CharField(max_length=500, blank=False, null=False)
    last_name = models.CharField(max_length=500, blank=False, null=False)
    email = models.CharField(max_length=500, blank=False, null=False)
    company_name = models.CharField(max_length=500, blank=False, null=False)
    location = models.CharField(max_length=500, blank=False, null=False)
    url = models.CharField(max_length=2000, blank=False, null=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company_name}"