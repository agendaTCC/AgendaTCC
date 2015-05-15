from haystack import indexes
from models import Banca


class BancaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document = True, use_template=True)
    
    
    def get_model(self):
        return Banca
    
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()