from rest_framework import serializers
from .models import Project, Contract
from apps.authentication.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    manager_details = UserSerializer(source='manager', read_only=True)
    team_members_details = UserSerializer(source='team_members', many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'code', 'description', 'status', 'priority',
            'client', 'location', 'address', 'manager', 'manager_details',
            'team_members', 'team_members_details', 'start_date', 'end_date',
            'budget', 'metadata', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProjectListSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.full_name', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'code', 'status', 'priority',
            'client', 'manager', 'manager_name', 'start_date', 'end_date'
        ]


class ContractSerializer(serializers.ModelSerializer):
    project_details = ProjectListSerializer(source='project', read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Contract
        fields = [
            'id', 'project', 'project_details', 'contract_number', 'title',
            'description', 'status', 'contractor', 'contract_value',
            'sign_date', 'start_date', 'end_date', 'terms', 'attachments',
            'created_by', 'created_by_details', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
