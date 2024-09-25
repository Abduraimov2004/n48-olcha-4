from rest_framework.generics import ListCreateAPIView


from olcha.models import Category, Group
from olcha.serializers import CategorySerializer, GroupSerializer


class GroupListApiView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

