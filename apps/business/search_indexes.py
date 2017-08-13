from haystack import indexes
from .models import Business, Food


class BusinessIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Business

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class FoodIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Food

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
