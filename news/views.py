from rest_framework.response import Response
from rest_framework.views import APIView
from news.models import News
from news.serializers import NewsSerializer


class NewsList(APIView):

    def get(self, request):
        tags = request.query_params.get('tags', None)
        news = News.objects.all()

        if tags is not None:
            tags = tags.split(',')
            news = news.filter(tags__name__in=tags)

        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)
