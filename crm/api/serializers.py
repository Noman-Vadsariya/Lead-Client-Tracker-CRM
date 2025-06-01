from rest_framework import serializers
from django.contrib.auth.models import User
from taggit.serializers import TagListSerializerField
from ..models import Lead, Client, Note, FollowUp


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class NoteSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'content', 'lead', 'client',
                  'created_by', 'created_at', 'updated_at')
        read_only_fields = ('created_by', 'created_at', 'updated_at')


class FollowUpSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = FollowUp
        fields = ('id', 'lead', 'client', 'scheduled_date', 'status',
                  'notes', 'assigned_to', 'created_at', 'updated_at')
        read_only_fields = ('assigned_to', 'created_at', 'updated_at')


class LeadSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    assigned_to = UserSerializer(read_only=True)
    notes = NoteSerializer(many=True, read_only=True)
    followups = FollowUpSerializer(many=True, read_only=True)

    class Meta:
        model = Lead
        fields = ('id', 'name', 'email', 'phone', 'company', 'status', 'source',
                  'assigned_to', 'next_follow_up', 'tags', 'notes', 'followups',
                  'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class ClientSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    assigned_to = UserSerializer(read_only=True)
    notes = NoteSerializer(many=True, read_only=True)
    followups = FollowUpSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'name', 'email', 'phone', 'company', 'status',
                  'assigned_to', 'next_follow_up', 'tags', 'notes', 'followups',
                  'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
