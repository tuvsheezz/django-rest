from django.contrib import admin
from .models import Legalact, Plan, PlanGoal, PlanAction, PlanTask, PlanOutcome

# Register your models here.

admin.site.register(Legalact)
admin.site.register(Plan)
admin.site.register(PlanGoal)
admin.site.register(PlanAction)
admin.site.register(PlanTask)
admin.site.register(PlanOutcome)
