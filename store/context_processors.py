from .models import Variation

def size_chart(request):
    size = Variation.objects.all()
    return dict(size=size)