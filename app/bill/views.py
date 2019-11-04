from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from core.models import Bill, Billview, Subscribe

from bill import serializers


class CustomPaginaction(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BillViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage Bills in the database"""
    queryset = Bill.objects.all()
    serializer_class = serializers.BillSerializer
    pagination_class = CustomPaginaction


class BillDetailViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage Detailed Bills in the database"""
    queryset = Billview.objects.all()
    serializer_class = serializers.BillDetailSerializer
    pagination_class = CustomPaginaction

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Enable the id and committee params"""
        id = self.request.query_params.get('id')
        committee = self.request.query_params.get('committee')
        if id:
            ids = self._params_to_ints(id)
            self.queryset = self.queryset.filter(billid__in=ids)
        if committee:
            self.queryset = self.queryset.filter(committeename=committee)
        return self.queryset.order_by('-billno')


class SubscribeViewSet(viewsets.ModelViewSet):
    """Manage Subscribes in the database"""
    queryset = Subscribe.objects.all()
    serializer_class = serializers.SubscriptionSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        return self.queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    def perform_create(self, serializer):
        """Create a new subscription"""
        serializer.save(user=self.request.user)
