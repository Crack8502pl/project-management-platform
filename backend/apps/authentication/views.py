from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import update_session_auth_hash, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Role
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    ChangePasswordSerializer, RoleSerializer
)
import logging

logger = logging.getLogger('authentication')


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing roles.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'email', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update current user profile."""
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            serializer = UserUpdateSerializer(
                request.user,
                data=request.data,
                partial=request.method == 'PATCH'
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(UserSerializer(request.user).data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password."""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': 'Wrong password.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        update_session_auth_hash(request, user)
        
        return Response({'detail': 'Password updated successfully.'})


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Logowanie użytkownika przez Active Directory lub lokalną bazę.
    """
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '')
    
    if not username or not password:
        return Response(
            {'error': 'Username i password są wymagane'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if '@' in username:
        username = username.split('@')[0]
    
    logger.info(f"Login attempt for user: {username}")
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        if not user.is_active:
            logger.warning(f"Inactive user tried to login: {username}")
            return Response(
                {'error': 'Konto użytkownika jest nieaktywne'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        refresh = RefreshToken.for_user(user)
        
        if not user.role:
            logger.warning(f"User {username} logged in without role assigned")
        
        logger.info(f"✅ User {username} logged in successfully (source: {user.auth_source})")
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role.name if user.role else None,
                'auth_source': user.auth_source,
                'phone': user.phone or '',
            }
        })
    else:
        logger.warning(f"❌ Failed login attempt for user: {username}")
        return Response(
            {'error': 'Nieprawidłowy login lub hasło'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
def current_user_view(request):
    """
    Zwraca dane zalogowanego użytkownika
    """
    user = request.user
    return Response({
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role.name if user.role else None,
        'auth_source': user.auth_source,
        'phone': user.phone or '',
    })
