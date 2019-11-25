from django.contrib.syndication.views import Feed
from django.urls import reverse
from news.models import news 

class LatestNewsFeed(Feed):
    
    title = "latest news"
    link = ""
    description = "latest news"

    def items(self):
        return news.objects.order_by('-date')[:30]

    def item_title(self,item):
        return item.news_title

    def item_description(self,item):
        return item.text[:20]

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('news:detail',kwargs={'news_id':item.id})