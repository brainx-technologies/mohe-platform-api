import django.contrib.auth.password_validation as validators
from rest_framework import serializers

from mohe.client.models import User


class UserSerializer(serializers.ModelSerializer):
    admin_url = serializers.SerializerMethodField()
    dwh_url = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    def get_admin_url(self, obj):
        return 'deprecated'

    def get_team_name(self, obj):
        return 'deprecated'

    def get_dwh_url(self, obj):
        return 'deprecated'

    def get_token(self, obj):
        return 'deprecated'

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'birthday', 'sex', 'team_name', 'admin_url', 'dwh_url',
                  'token')


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
