from rest_framework.generics import get_object_or_404
from reviews.models import Review


def get_review_object(self):
    review_id = self.kwargs.get('review_id')
    return get_object_or_404(Review, pk=review_id)
