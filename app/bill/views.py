from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from core.models import Committee, Bill, Billview, Subscribe, Bookmark

from bill import serializers


class CustomPaginaction(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CommitteeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage Committees in the database"""
    queryset = Committee.objects.all()
    serializer_class = serializers.CommitteeSerializer
    pagination_class = CustomPaginaction

    def get_queryset(self):
        committee = self.request.query_params.get('committee')
        if committee:
            self.queryset = self.queryset.filter(committee=committee)
        return self.queryset.order_by('id')


class BillViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage Bills in the database"""
    queryset = Bill.objects.all()
    serializer_class = serializers.BillSerializer
    pagination_class = CustomPaginaction
    search_fields = ['bill']
    filter_backends = (filters.SearchFilter,)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Enable the id params"""
        self.queryset = self.queryset.exclude(count__isnull=True)
        id = self.request.query_params.get('id')
        committee = self.request.query_params.get('committee')
        sortKey = self.request.query_params.get('sortKey')
        bill = self.request.query_params.get('bill')
        if id:
            ids = self._params_to_ints(id)
            self.queryset = self.queryset.filter(id__in=ids)
        if committee:
            committees = self._params_to_ints(committee)
            self.queryset = self.queryset.filter(committee_id__in=committees)
        if sortKey:
            if sortKey=='bill':
                return self.queryset.order_by(f'{sortKey}')
            return self.queryset.order_by(f'-{sortKey}')
        if bill:
            self.queryset = self.queryset.filter(bill=bill)
        return self.queryset.order_by('-id')


class BillViewViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage Detailed Bills in the database"""
    queryset = Billview.objects.all()
    serializer_class = serializers.BillViewSerializer
    pagination_class = CustomPaginaction
    search_fields = ['summarycontent']
    filter_backends = (filters.SearchFilter,)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Enable the id params"""
        bill = self.request.query_params.get('bill')
        committee = self.request.query_params.get('committee')
        billno = self.request.query_params.get('billno')
        finished = self.request.query_params.get('finished')
        billstep = self.request.query_params.get('billstep')
        generalresult = self.request.query_params.get('generalresult')
        status = self.request.query_params.get('status')
        sortKey = self.request.query_params.get('sortKey')
        if bill:
            ids = self._params_to_ints(bill)
            self.queryset = self.queryset.filter(bill_id__in=ids)
        if committee:
            committees = self._params_to_ints(committee)
            self.queryset = self.queryset.filter(committee_id__in=committees)
        if billno:
            billnos = self._params_to_ints(billno)
            self.queryset = self.queryset.filter(billno__in=billnos)
        if finished:
            if finished=='':
                self.queryset = self.queryset.filter(finished=finished)
            else:
                self.queryset = self.queryset.filter(finished=bool(int(finished)))
        if status:
            self.queryset = self.queryset.filter(status=status)
        if billstep:
            self.queryset = self.queryset.filter(billstep=billstep)
        if generalresult:
            self.queryset = self.queryset.filter(generalresult=generalresult)
        if sortKey:
            if sortKey in ['billno', 'lastupdated']:
                return self.queryset.order_by(f'-{sortKey}')
            return self.queryset.order_by(f'{sortKey}')
        return self.queryset.order_by('-billno')


class BillViewCoverViewSet(viewsets.ModelViewSet):
    """Manage Detailed Bills in the database"""
    queryset = Billview.objects.all()
    serializer_class = serializers.BillViewCoverSerializer
    pagination_class = CustomPaginaction

    def get_queryset(self):
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


class BookmarkViewSet(viewsets.ModelViewSet):
    """Manage Bookmarks in the database"""
    queryset = Bookmark.objects.all()
    serializer_class = serializers.BookmarkSerializer

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
