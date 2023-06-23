from django.http import Http404
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
    API to manage the authenticated user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        # the api only allows access to the authenticated user
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        # make sure the correct pk is used
        if self.request.user.pk != int(self.kwargs['pk']):
            raise Http404()
        return self.request.user

    def get_serializer_class(self):
        # password action has its own serializer
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

    @action(detail=True, methods=['post'], name='Change Password')
    def password(self, request, pk=None):
        """
        Change the user password.
        """
        self.object = self.get_object()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.update()
            return Response({})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    API to register new users. After submit a verification email will be send to create a password and activate the account.
    """

    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return User.objects.none()
