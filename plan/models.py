from django.db import models

# Create your models here.
class Legalact(models.Model):
    name = models.CharField(max_length=200,blank=False)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Plan(models.Model):
    year = models.CharField(max_length=4,blank=True,null=True)
    is_yearly_plan = models.NullBooleanField(default=True)
    organization_name = models.CharField(max_length=50,blank=True,null=True)
    department_name = models.CharField(max_length=50,blank=True,null=True)
    legalacts = models.ManyToManyField(Legalact, related_name="legalacts", blank=True)
    author_name = models.CharField(max_length=50)
    author_id = models.IntegerField(blank=False)
    authorized_user_name = models.CharField(max_length=50,blank=True,null=True)
    author_id = models.IntegerField(blank=True)
    is_draft = models.NullBooleanField(default=True)
    is_authorized = models.NullBooleanField(default=False)
    is_deleted = models.NullBooleanField(default=False)
    authorized_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'PK {} No {}, {}, {}'.format(self.pk, self.year, self.organization_name, self.department_name )

class PlanGoal(models.Model):
    plan = models.ForeignKey(Plan, default=0, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=True)
    months = models.CharField(max_length=200,blank=True)
    coherence = models.TextField(blank=True)
    fund = models.TextField(blank=True)
    baselevel = models.TextField(blank=True)
    criteria = models.TextField(blank=True)
    season1 = models.TextField(blank=True)
    season2 = models.TextField(blank=True)
    season3 = models.TextField(blank=True)
    season4 = models.TextField(blank=True)
    outcomename = models.CharField(max_length=200,blank=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PlanAction(models.Model):
    plan_goal = models.ForeignKey(PlanGoal, default=0, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PlanTask(models.Model):
    plan_action = models.ForeignKey(PlanAction, default=0, on_delete=models.CASCADE)
    season = models.IntegerField(blank=False,default=-1)
    text = models.TextField(blank=True)
    months = models.CharField(max_length=200,blank=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PlanOutcome(models.Model):
    plan_goal = models.ForeignKey(PlanGoal, default=0, on_delete=models.CASCADE)
    name = models.TextField(blank=True)
    measurement = models.TextField(blank=True)
    base = models.TextField(blank=True)
    halfyear = models.TextField(blank=True)
    endofyear = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
