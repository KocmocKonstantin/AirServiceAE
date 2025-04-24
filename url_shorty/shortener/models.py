from django.db import models
import random
import string


class URL(models.Model):
    original_url = models.URLField(max_length=500)
    short_code = models.CharField(max_length=6, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    access_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.original_url} -> {self.short_code}"
    
    @classmethod
    def generate_short_code(cls):
        """Generate a random 6-character code of letters and numbers"""
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choice(characters) for _ in range(6))
            if not cls.objects.filter(short_code=short_code).exists():
                return short_code
