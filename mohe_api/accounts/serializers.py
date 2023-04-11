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
        fields = ('id', 'first_name', 'last_name', 'email', 'team_name', 'admin_url', 'dwh_url', 'token')
