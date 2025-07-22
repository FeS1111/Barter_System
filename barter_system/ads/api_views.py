from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer


class AdListCreateView(generics.ListCreateAPIView):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'category', 'condition']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        ad = self.get_object()
        if ad.user != self.request.user:
            raise PermissionDenied("Вы не являетесь автором объявления!")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не являетесь автором объявления!")
        instance.delete()


class ExchangeProposalListView(generics.ListCreateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ad_sender__user__username', 'ad_receiver__user__username', 'status']
    ordering_fields = ['created_at', 'status']

    def get_queryset(self):
        qs = super().get_queryset()
        sender = self.request.query_params.get('sender')
        receiver = self.request.query_params.get('receiver')
        status = self.request.query_params.get('status')
        if sender:
            qs = qs.filter(ad_sender__user__username__icontains=sender)
        if receiver:
            qs = qs.filter(ad_receiver__user__username__icontains=receiver)
        if status:
            qs = qs.filter(status=status)
        return qs


class ExchangeProposalListCreateView(generics.ListCreateAPIView):
    queryset = ExchangeProposal.objects.all().order_by('-created_at')
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['comment', 'status']


class ExchangeProposalRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]