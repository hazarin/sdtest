from rest_framework import serializers
from . import models


class PrecedentsListField(serializers.RelatedField):
    def to_internal_value(self, data):
        key = list(data.keys())[0]
        try:
            precedent_cat = models.PrecedentCatalog.objects.get(name=key)
        except models.PrecedentCatalog.DoesNotExist as e:
            precedent_cat = models.PrecedentCatalog.objects.create(name=key)
        attitude = None
        for v, k in models.Precedent.ATTITUDE_CHOICES:
            if data[key]['attitude'] == k:
                attitude = v
                break
        return {
            'precedent': precedent_cat,
            'attitude': attitude,
            'importance': data[key]['importance'],
        }

    def to_representation(self, value):
        return {
            value.precedent.name: {
                'attitude': value.get_attitude_display(),
                'importance': value.importance
            }
        }


class ParticipantSerializer(serializers.ModelSerializer):
    precedents = PrecedentsListField(queryset=models.Precedent.objects.all(), many=True, read_only=False)

    class Meta:
        model = models.Participant
        fields = ('id', 'name', 'precedents')

    def create(self, validated_data):
        precedents = validated_data.pop('precedents')
        participant = models.Participant.objects.create(**validated_data)
        for precedent in precedents:
            models.Precedent.objects.create(participant=participant, **precedent)
        return participant

    def update(self, instance, validated_data):
        precedents = validated_data.pop('precedents')
        precedents_items_dict = dict((i.precedent.name, i) for i in instance.precedents.all())
        for precedent in precedents:
            if precedents_items_dict.get(precedent['precedent'].name) is not None:
                prom_precedent = precedents_items_dict.pop(precedent['precedent'].name)
                precedent.pop('precedent')
                for key in precedent.keys():
                    setattr(prom_precedent, key, precedent[key])
                prom_precedent.save()
            else:
                models.Precedent.objects.create(participant=instance, **precedent)

        # удаляем элементы отсутствующте в PUT request
        if not self.partial and len(precedents_items_dict) > 0:
            for item in precedents_items_dict.values():
                item.delete()

        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
