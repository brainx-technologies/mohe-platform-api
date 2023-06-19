from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from mohe.client.models import User
from mohe_api.accounts.serializers import UserSerializer, PasswordSerializer, RegistrationSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    This endpoint returns the user profile for the authenticated user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'password':
            return PasswordSerializer
        return UserSerializer

    @action(detail=True, methods=['put', 'post', 'get'], name='Change Password')
    def password(self, request, pk=None):
        self.object = self.get_object()

        response = {}

        if self.request.method in ('POST', 'PUT'):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.update()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(response)


class RegistrationViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return User.objects.none()

