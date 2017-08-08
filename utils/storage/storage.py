import os
import random
import time

from django.core.files.storage import FileSystemStorage


class ImgStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        ext = os.path.splitext(name)[1]
        d = os.path.dirname(name)
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%d' % random.randint(0, 100)
        name = os.path.join(d, fn + ext)
        return super(ImgStorage, self)._save(name, content)

