from django.db import models
from datetime import datetime, timedelta


# Create your models here.
def get_deadline():
    return datetime.now() + timedelta(days=21)

class Poll(models.Model):
    name = models.CharField(max_length=200,blank=False)
    is_draft = models.NullBooleanField(default=True)
    is_deleted = models.NullBooleanField(default=False)
    deadline = models.DateTimeField(default=get_deadline)
    can_add_options = models.NullBooleanField(default=True)
    can_check_multiple_option = models.NullBooleanField(default=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=False)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    user_name = models.CharField(max_length=100)
    user_id = models.IntegerField(blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class PollOptionVote(models.Model):
    poll = models.ForeignKey(Poll, null=True, on_delete=models.CASCADE)
    poll_option = models.ForeignKey(PollOption, null=True, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    user_id = models.IntegerField(blank=False)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.poll_option
