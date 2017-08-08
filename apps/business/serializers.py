from rest_framework import serializers

from .models import Business, Food


class FoodSerializer(serializers.HyperlinkedModelSerializer):
    business = serializers.HyperlinkedRelatedField(view_name='business_detail_api', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='food_detail_api')

    class Meta:
        model = Food
        fields = (
            'business',
            'pk',
            'url',
            'name',
            'image',
            'price',
            'can_reserve'
        )


class BusinessSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='business_detail_api')
    foodlist = serializers.HyperlinkedRelatedField(many=True, view_name='food_detail_api', read_only=True)

    class Meta:
        model = Business
        fields = (
            'pk',
            'url',
            'name',
            'position',
            'floor',
            'type',
            'image',
            'average',
            'foodlist',
        )
