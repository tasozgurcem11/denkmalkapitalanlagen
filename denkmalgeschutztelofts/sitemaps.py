from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    protocol = "https"
    def items(self):
        return ['denkmalgeschutztelofts:index','denkmalgeschutztelofts:kaiserdicke','denkmalgeschutztelofts:rubenstrasse','denkmalgeschutztelofts:afa', 'denkmalgeschutztelofts:covid', 'denkmalgeschutztelofts:kontakt', 'denkmalgeschutztelofts:newsletter_abonnieren']

    def location(self, item):
        return reverse(item)