from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsAdminOrOwner
from .serializers import ParticipantSerializer, CompatibleSerializer
from .models import Participant


# Create your views here.
class ParticipantViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return participant info.

    list:
    Return a list of participants.

    create:
    Create participant info for current user.

    update:
    Update participant info.

    partial_update:
    Partial update participant info.

    delete:
    Delete participant info.

    compatible:
    Get compatible participants info for current user.
    """
    serializer_classes = {
        'compatible': CompatibleSerializer,
    }
    default_serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @action(detail=False)
    def compatible(self, request):
        user = request.user
        # check weight...
        compatible_users = list(filter(lambda item: item.weight >= 75, Participant.objects.compatible(user)))

        serializer = self.get_serializer(compatible_users, many=True)
        return Response(serializer.data)


class ParticipantView(RetrieveAPIView):
    """
    Get participant info for current user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj
