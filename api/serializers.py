from rest_framework import serializers
from . import models


class PrecedentsListField(serializers.RelatedField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return {
            value.precedent.name:{
                'attitude': value.get_attitude_display(),
                'importance': value.importance
            }
        }


class ParticipantSerializer(serializers.ModelSerializer):
    precedents = PrecedentsListField(many=True, read_only=True)

    class Meta:
        model = models.Participant
        fields = ('id', 'name', 'precedents')
