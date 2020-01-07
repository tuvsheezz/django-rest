from django.contrib import admin
from .models import Poll, PollOption, PollOptionVote
# Register your models here.

admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(PollOptionVote)
