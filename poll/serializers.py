from rest_framework import serializers, fields
from .models import Poll, PollOption, PollOptionVote
import json

class PollOptionVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOptionVote
        fields = ['id', 'user_id', 'user_name', 'poll_option', 'poll']

class PollOptionSerializer(serializers.ModelSerializer):
    option_votes = PollOptionVoteSerializer(source='polloptionvote_set', many=True, read_only=True)
    class Meta:
        model = PollOption
        fields = ['id', 'name', 'option_votes', 'poll', 'user_id', 'user_name']

class PollSerializer(serializers.ModelSerializer):
    pollOptions = PollOptionSerializer(source='polloption_set', many=True, read_only=True)
    deadline = fields.DateTimeField(input_formats=['%Y-%m-%d'])
    class Meta:
        model = Poll
        fields = ['id', 'name', 'is_draft', 'is_deleted', 'can_add_options', 'can_check_multiple_option', 'deadline', 'pollOptions']
