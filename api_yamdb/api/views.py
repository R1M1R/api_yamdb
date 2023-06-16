from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)

from reviews.models import Review, Title

from api.permissions import (
    IsAdminModeratorAuthorOrReadOnly,
)

from .serializers import (
    ReviewSerializer,
    CommentSerializer
)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        """Получаем отзывы связанных произведений."""
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        """Создаём новый отзыв для текущего произведения."""
        pk = self.kwargs.get('title_id')
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=pk)
        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        """Получаем комментарии связанных отзывов."""
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        """Создаём новый комментарий для текущего отзыва."""
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
