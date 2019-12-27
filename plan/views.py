from .models import Legalact, Plan, PlanGoal, PlanAction, PlanTask, PlanOutcome
from rest_framework import pagination, viewsets
from .serializers import LegalactSerializer, PlanSerializer, PlanGoalSerializer, PlanActionSerializer, PlanTaskSerializer, PlanOutcomeSerializer

class PlanPagination(pagination.PageNumberPagination):
    page_size = 20

class LegalactViewSet(viewsets.ModelViewSet):
    queryset = Legalact.objects.all().order_by('-created_date')
    serializer_class = LegalactSerializer

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.exclude(is_deleted=True).order_by('-created_date')
    serializer_class = PlanSerializer

class PlanGoalViewSet(viewsets.ModelViewSet):
    queryset = PlanGoal.objects.all().order_by('id')
    serializer_class = PlanGoalSerializer

class PlanActionViewSet(viewsets.ModelViewSet):
    queryset = PlanAction.objects.all().order_by('id')
    serializer_class = PlanActionSerializer

class PlanTaskViewSet(viewsets.ModelViewSet):
    queryset = PlanTask.objects.all().order_by('id')
    serializer_class = PlanTaskSerializer

class PlanOutcomeViewSet(viewsets.ModelViewSet):
    queryset = PlanOutcome.objects.all().order_by('id')
    serializer_class = PlanOutcomeSerializer
