from .models import Poll, PollOption, PollOptionVote
from datetime import datetime
from rest_framework.response import Response
from rest_framework import pagination, viewsets, generics, status
from .serializers import PollSerializer, PollOptionSerializer, PollOptionVoteSerializer
import json

class PollPagination(pagination.PageNumberPagination):
    page_size = 10

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by('-created_date')
    serializer_class = PollSerializer
    pagination_class = PollPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        poll = serializer.save(
            name=request.data.get('name'),
            is_draft=True if request.data.get('is_draft') == 'true' else False,
            is_deleted=True if request.data.get('is_deleted') == 'true' else False,
            deadline=datetime.strptime(request.data.get('deadline'),'%Y-%m-%d'),
            can_add_options=True if request.data.get('can_add_options') == 'true' else False,
            can_check_multiple_option=True if request.data.get('can_check_multiple_option') == 'true' else False
        )

        for pollO in json.loads(request.data.get('pollOptions')):
            if pollO["name"].strip() != "":
                pollOption = PollOption.objects.create(
                    poll=poll,
                    name=pollO['name'].strip(),
                    user_id=pollO['user_id'],
                    user_name=pollO['user_name']
                )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PollOptionViewSet(viewsets.ModelViewSet):
    queryset = PollOption.objects.all().order_by('-created_date')
    serializer_class = PollOptionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        poll = Poll.objects.filter(id = int(request.data.get('poll'))).first()

        serializer.save(
            name=request.data.get('name').strip(),
            user_id=request.data.get('user_id'),
            user_name=request.data.get('user_name'),
            poll=poll
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PollOptionVoteViewSet(viewsets.ModelViewSet):
    queryset = PollOptionVote.objects.all().order_by('-created_date')
    serializer_class = PollOptionVoteSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        poll = Poll.objects.filter(id = int(request.data.get('poll'))).first()
        poll_option = PollOption.objects.filter(id = int(request.data.get('poll_option'))).first()

        if poll.can_check_multiple_option == False:
            PollOptionVote.objects.filter(poll=poll,user_id=request.data.get('user_id')).delete()

        serializer.save(
            user_id=request.data.get('user_id'),
            user_name=request.data.get('user_name'),
            poll=poll,
            poll_option=poll_option
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
