from django.db.models import fields
from rest_framework import serializers
from .models import Submission, User
import uuid

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'display_name', 'points', 'rank']


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['score_worth', 'user_id', 'timestamp']


    
    """user_id = serializers.UUIDField(format="hex_verbose")
    display_name = serializers.CharField(max_length=40)
    points = serializers.IntegerField()
    rank = serializers.IntegerField()

    def create(self, validated_data):
        return User.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.points = validated_data.get('points', instance.points)
        instance.rank = validated_data.get('user_id', instance.rank)
        instance.save()
        return instance"""