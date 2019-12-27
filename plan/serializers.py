from rest_framework import serializers
from .models import Legalact, Plan, PlanGoal, PlanAction, PlanTask, PlanOutcome
import json

class LegalactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legalact
        fields = ['id', 'name']

class PlanTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlanTask
        fields = ['id', 'plan_action_id', 'season', 'text', 'months', 'created_date', 'updated_at']

class PlanActionSerializer(serializers.HyperlinkedModelSerializer):
    plantasks = PlanTaskSerializer(source='plantask_set', many=True, read_only=True)
    class Meta:
        model = PlanAction
        fields = ['id', 'plan_goal_id', 'name', 'plantasks', 'created_date', 'updated_at']

class PlanOutcomeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlanOutcome
        fields = ['id', 'plan_goal_id', 'name', 'measurement', 'base', 'halfyear', 'endofyear', 'created_date', 'updated_at']

class PlanGoalSerializer(serializers.HyperlinkedModelSerializer):
    planactions = PlanActionSerializer(source='planaction_set', many=True, read_only=True)
    planoutcomes = PlanOutcomeSerializer(source='planoutcome_set', many=True, read_only=True)
    class Meta:
        model=PlanGoal
        fields = ['id', 'plan_id', 'name', 'months', 'coherence', 'fund', 'baselevel', 'criteria', 'season1', 'season2', 'season3', 'season4', 'planactions', 'outcomename', 'planoutcomes', 'created_date', 'updated_at']

class PlanSerializer(serializers.HyperlinkedModelSerializer):
    plangoals = PlanGoalSerializer(source='plangoal_set', many=True, read_only=True)
    legalacts = LegalactSerializer(many=True, read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'year', 'is_yearly_plan', 'organization_name', 'department_name', 'author_name', 'author_id', 'authorized_user_name', 'is_draft', 'is_authorized', 'is_deleted', 'authorized_date', 'plangoals', 'legalacts', 'created_date', 'updated_at']

    def create(self, validated_data):
        #create post
        plan = Plan.objects.create(
            year=validated_data.get('year'),
            is_yearly_plan=validated_data.get('is_yearly_plan'),
            organization_name=validated_data.get('organization_name'),
            department_name=validated_data.get('department_name'),
            author_name=validated_data.get('author_name'),
            author_id=validated_data.get('author_id'),
            is_draft=validated_data.get('is_draft'),
            is_deleted=validated_data.get('is_deleted')
        )

        #handle legalacts
        legalacts_data = []
        if "legalacts_data" in dict(self.context.get('view').request.POST):
            legalacts_data = json.loads(self.context.get('view').request.POST['legalacts_data'])

        existing_legalacts_list = []
        for l_data in Legalact.objects.all():
            existing_legalacts_list.append(l_data.name)

        legalacts = []
        for l_data in legalacts_data:
            if not l_data["name"] in existing_legalacts_list:
                Legalact.objects.create(name=l_data["name"])
            legalacts.append(Legalact.objects.filter(name=l_data["name"])[0])

        plan.legalacts.set(legalacts)

        #handle plangoals
        plangoals_data = []
        if "plangoals_data" in dict(self.context.get('view').request.POST):
            plangoals_data = json.loads(self.context.get('view').request.POST['plangoals_data'])

        for plangoal_data in plangoals_data:
            plangoal = PlanGoal.objects.create(
                plan=plan,
                name=plangoal_data["name"],
                months=plangoal_data["months"],
                coherence=plangoal_data["coherence"],
                fund=plangoal_data["fund"],
                baselevel=plangoal_data["baselevel"],
                criteria=plangoal_data["criteria"],
                season1=plangoal_data["season1"],
                season2=plangoal_data["season2"],
                season3=plangoal_data["season3"],
                season4=plangoal_data["season4"],
                outcomename=plangoal_data["outcomename"]
            )

            #handle planoutcomes
            for outcome in plangoal_data["planoutcomes"]:
                if outcome["name"] != "":
                    PlanOutcome.objects.create(
                        plan_goal=plangoal,
                        name=outcome["name"],
                        measurement=outcome["measurement"],
                        base=outcome["base"],
                        halfyear=outcome["halfyear"],
                        endofyear=outcome["endofyear"]
                    )

            #handle planactions
            for planaction_data in plangoal_data["planactions"]:
                planaction = PlanAction.objects.create(
                    plan_goal=plangoal,
                    name=planaction_data["name"]
                )
                #handle plantasks
                for plantask_data in planaction_data["plantasks"]:
                    if plantask_data["text"] != "":
                        PlanTask.objects.create(
                            plan_action=planaction,
                            season=plantask_data["season"],
                            text=plantask_data["text"],
                            months=plantask_data["months"]
                        )
        return plan

    def update(self, instance, validated_data):
        instance.year=validated_data.get('year')
        instance.is_yearly_plan=validated_data.get('is_yearly_plan')
        instance.organization_name=validated_data.get('organization_name')
        instance.department_name=validated_data.get('department_name')
        instance.author_name=validated_data.get('author_name')
        instance.author_id=validated_data.get('author_id')
        instance.is_draft=validated_data.get('is_draft')
        instance.is_deleted=validated_data.get('is_deleted')

        instance.save()

        #handle legalacts
        legalacts_data = []
        if "legalacts_data" in dict(self.context.get('view').request.POST):
            legalacts_data = json.loads(self.context.get('view').request.POST['legalacts_data'])

        existing_legalacts_list = []
        for l_data in Legalact.objects.all():
            existing_legalacts_list.append(l_data.name)

        legalacts = []
        for l_data in legalacts_data:
            if not l_data["name"] in existing_legalacts_list:
                Legalact.objects.create(name=l_data["name"])
            legalacts.append(Legalact.objects.filter(name=l_data["name"])[0])

        instance.legalacts.set(legalacts)

        #handle plangoals
        PlanGoal.objects.filter(plan=instance).delete()

        plangoals_data = []
        if "plangoals_data" in dict(self.context.get('view').request.POST):
            plangoals_data = json.loads(self.context.get('view').request.POST['plangoals_data'])

        for plangoal_data in plangoals_data:
            plangoal = PlanGoal.objects.create(
                plan=instance,
                name=plangoal_data["name"],
                months=plangoal_data["months"],
                coherence=plangoal_data["coherence"],
                fund=plangoal_data["fund"],
                baselevel=plangoal_data["baselevel"],
                criteria=plangoal_data["criteria"],
                season1=plangoal_data["season1"],
                season2=plangoal_data["season2"],
                season3=plangoal_data["season3"],
                season4=plangoal_data["season4"],
                outcomename=plangoal_data["outcomename"]
            )
            
            #handle planoutcomes
            for outcome in plangoal_data["planoutcomes"]:
                if outcome["name"] != "":
                    PlanOutcome.objects.create(
                        plan_goal=plangoal,
                        name=outcome["name"],
                        measurement=outcome["measurement"],
                        base=outcome["base"],
                        halfyear=outcome["halfyear"],
                        endofyear=outcome["endofyear"]
                    )
            #handle planactions
            for planaction_data in plangoal_data["planactions"]:
                planaction = PlanAction.objects.create(
                    plan_goal=plangoal,
                    name=planaction_data["name"]
                )
                #handle plantasks
                for plantask_data in planaction_data["plantasks"]:
                    if plantask_data["text"] != "":
                        PlanTask.objects.create(
                            plan_action=planaction,
                            season=plantask_data["season"],
                            text=plantask_data["text"],
                            months=plantask_data["months"]
                        )
        return instance
