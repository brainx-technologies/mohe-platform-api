import logging

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from mohe.client.models import User
from mohe_api.accounts.serializers import UserSerializer, ChangePasswordSerializer, RegistrationSerializer, \
    ForgotPasswordSerializer

LOGGER = logging.getLogger(__name__)


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
        if 'pk' in self.kwargs:
            if self.request.user.pk != int(self.kwargs.get('pk')):
                raise Http404()
        else:
            raise Http404()
        return self.request.user

    def get_serializer_class(self):
        # password action has its own serializer
        if self.action == 'forgot_password':
            return ForgotPasswordSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        """
        Returns the user which is logged in.
        """
        user = self.get_queryset().first()
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], name='Change Password')
    def change_password(self, request, pk=None):
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

    @action(detail=False, methods=['post'], name='Forgot Password')
    def forgot_password(self, request, pk=None):
        """
        Change the user password.
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                form = PasswordResetForm(serializer.validated_data)
                form.is_valid()

                opts = {
                    "use_https": self.request.is_secure(),
                    "token_generator": default_token_generator,
                    "from_email": None,
                    "email_template_name": "registration/password_reset_email.html",
                    "subject_template_name": "registration/password_reset_subject.txt",
                    "request": self.request,
                    "html_email_template_name": None,
                    "extra_email_context": None,
                }

                form.save(**opts)
            except Exception as e:
                LOGGER.exception("error sending password email.")

        else:
            return Response(serializer.errors)

        return Response({'result': 'success', 'message':
            'We’ve emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly.'
            'If you don’t receive an email, please make sure you’ve entered the address you registered with, and check your spam folder.'
                         })


class RegistrationViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    API to register new users. After submit a verification email will be send to create a password and activate the account.
    """

    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return User.objects.none()
