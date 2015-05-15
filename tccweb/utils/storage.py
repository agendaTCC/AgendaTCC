import unicodedata

from django.core.files.storage import FileSystemStorage

class ASCIIFileSystemStorage(FileSystemStorage):
    """
    Convert unicode characters in name to ASCII characters.
    """
    def get_valid_name(self, name):
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        name = unicode(name)
        return super(ASCIIFileSystemStorage, self).get_valid_name(name)