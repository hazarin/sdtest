from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ParticipantSerializer
from .models import Participant


# Create your views here.
class ParticipantViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return participant precedents.

    list:
    Return a list of compatible participants.

    create:
    Create participant precedents list for user.

    update:
    Update participant precedents list for user.
    """
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super(ParticipantViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(ParticipantViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(ParticipantViewSet, self).update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(ParticipantViewSet, self).update(request, *args, **kwargs)
