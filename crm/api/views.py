from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User, Group
from import_export import resources
from ..models import Lead, Client, Note, FollowUp
from .serializers import (
    LeadSerializer, ClientSerializer, NoteSerializer, FollowUpSerializer,
    UserSerializer
)


class IsAssignedOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.assigned_to == request.user


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'assigned_to', 'tags']
    search_fields = ['name', 'email', 'company', 'notes']
    ordering_fields = ['created_at', 'next_follow_up', 'name']
    permission_classes = [permissions.IsAuthenticated, IsAssignedOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(assigned_to=self.request.user)

        # Filter for today's follow-ups
        if self.request.query_params.get('follow_up_today'):
            today = timezone.now().date()
            queryset = queryset.filter(next_follow_up__date=today)

        return queryset

    @action(detail=False, methods=['get'])
    def export(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        resource = resources.modelresource_factory(model=Lead)()
        dataset = resource.export(queryset)
        response = Response(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="leads.csv"'
        return response


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'assigned_to', 'tags']
    search_fields = ['name', 'email', 'company', 'notes']
    ordering_fields = ['created_at', 'next_follow_up', 'name']
    permission_classes = [permissions.IsAuthenticated, IsAssignedOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(assigned_to=self.request.user)

        # Filter for today's follow-ups
        if self.request.query_params.get('follow_up_today'):
            today = timezone.now().date()
            queryset = queryset.filter(next_follow_up__date=today)

        return queryset

    @action(detail=False, methods=['get'])
    def export(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        resource = resources.modelresource_factory(model=Client)()
        dataset = resource.export(queryset)
        response = Response(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="clients.csv"'
        return response


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['lead', 'client', 'created_by']
    search_fields = ['content']
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FollowUpViewSet(viewsets.ModelViewSet):
    queryset = FollowUp.objects.all()
    serializer_class = FollowUpSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'assigned_to', 'lead', 'client']
    search_fields = ['notes']
    ordering_fields = ['scheduled_date', 'created_at']
    permission_classes = [permissions.IsAuthenticated, IsAssignedOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(assigned_to=self.request.user) |
                Q(lead__assigned_to=self.request.user) |
                Q(client__assigned_to=self.request.user)
            )

        # Filter for today's follow-ups
        if self.request.query_params.get('follow_up_today'):
            today = timezone.now().date()
            queryset = queryset.filter(scheduled_date__date=today)

        return queryset

    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_staff', 'is_active', 'groups']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_role(self, request, pk=None):
        user = self.get_object()
        role = request.data.get('role')

        if not role:
            return Response(
                {'error': 'Role is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            group = Group.objects.get(name=role)
            user.groups.clear()
            user.groups.add(group)
            return Response({'status': 'role set'})
        except Group.DoesNotExist:
            return Response(
                {'error': 'Invalid role'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        password = request.data.get('password')

        if not password:
            return Response(
                {'error': 'Password is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(password)
        user.save()
        return Response({'status': 'password set'})

    def perform_create(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()
