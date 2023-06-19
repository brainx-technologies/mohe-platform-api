import django.contrib.auth.password_validation as validators
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers

from mohe.client.models import User, Organisation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'birthday', 'sex', 'mode', 'organisation_name')


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        validators.validate_password(password=value, user=user)
        return value

    def update(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class RegistrationSerializer(serializers.ModelSerializer):
    organisation_name = serializers.CharField(required=False)

    def validate_organisation_name(self, value):
        if Organisation.objects.filter(name=value).exists():
            raise serializers.ValidationError("Organisation name already taken.")
        return value

    def validate(self, data):
        if data['mode'] == 'personal':
            if data.get('organisation_name'):
                raise serializers.ValidationError({
                    'organisation_name': 'Organisation name must be empty in personal mode.'
                })

        if data['mode'] == 'professional':
            if data.get('organisation_name') in ('', None):
                raise serializers.ValidationError({
                    'organisation_name': 'Organisation is required in professional mode.'
                })

        return data

    def save(self, **kwargs):
        if 'organisation_name' in self.validated_data:
            organisation_name = self.validated_data.pop('organisation_name')
            if organisation_name:
                org = Organisation.objects.create(name=organisation_name)
                kwargs['organisation'] = org

        user = super().save(**kwargs)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        domain = settings.MOHE_DOMAIN
        subject = f'Complete your registration at {domain}'
        template = loader.get_template('registration/registration_mail.txt')
        context = dict(
            user=user,
            domain=domain,
            token=default_token_generator.make_token(user),
            uid=urlsafe_base64_encode(force_bytes(user.pk))
        )
        message = template.render(context)
        user.email_user(subject, message)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'birthday', 'sex', 'mode', 'organisation_name')
