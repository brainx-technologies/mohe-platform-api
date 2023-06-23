from django.http import Http404
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from mohe.client.models import User
from mohe_api.accounts.serializers import UserSerializer, PasswordSerializer, RegistrationSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    API to manage user accounts.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        user = self.get_queryset().filter(pk=self.kwargs['pk']).first()
        if user is None:
            raise Http404()
        return user

    def get_serializer_class(self):
        if self.action == 'password':
            return PasswordSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        """
        Returns the user which is logged in.
        """
        user = self.get_object()
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['put', 'post', 'get'], name='Change Password')
    def password(self, request, pk=None):
        """
        Change the user password.
        """
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
    """
    API to register new users. After submit a verification email will be send to create a password and activate the account.
    """

    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return User.objects.none()
