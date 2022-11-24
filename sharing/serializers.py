from rest_framework import serializers
from .models import User, Giver, Taker

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(
            work_email = validated_data['work_email'],
            fname = validated_data['fname'],
            lname = validated_data['lname'],
            contact = validated_data['contact']
        )

        user.save()
        return user

class GiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Giver
        fields = '__all__'

    def create(self, validated_data):
        giver = Giver(
            user = validated_data['user'],
            portion = validated_data['portion'],
            order_id = validated_data['order_id'],
            veg = validated_data['veg'],
            piece = validated_data['piece'],
            available = 1
        )

        giver.save()
        return giver

class TakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taker
        fields = '__all__'

    def create(self, validated_data):
        taker = Taker(
            user = validated_data['user'],
            req_portion = validated_data['req_portion'],
            got_food = validated_data['got_food'],
            veg_preference = validated_data['veg_preference']
        )

        taker.save()
        return taker