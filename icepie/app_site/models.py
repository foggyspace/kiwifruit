from django.db import models
from django.contrib import admin


class Task(models.Model):
    name = models.CharField(max_length=200)
    status = models.IntegerField()
    start_url = models.URLField()
    base = models.CharField(max_length=40)
    url_count = models.IntegerField()
    progress = models.TextField()
    spider_flag = models.IntegerField(default=1)
    robots_parsed = models.BooleanField(default=False)
    sitemap_parsed = models.BooleanField(default=False)
    reachable = models.BooleanField(default=False)
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "task"


class Url(models.Model):
    task_id = models.IntegerField()
    url = models.URLField(max_length=400)
    method = models.CharField(max_length=10)
    params = models.CharField(max_length=200, blank=True)
    referer = models.CharField(max_length=200, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "url"


class Result(models.Model):
    task_id = models.IntegerField()
    rule_id = models.IntegerField()
    risk = models.IntegerField(default=1)
    url = models.URLField()
    detail = models.TextField(blank=True)
    request = models.TextField(blank=True)
    response = models.TextField(blank=True)

    class Meta:
        db_table = "result"


class Rule(models.Model):
    rule_id = models.IntegerField()
    rule_name = models.CharField(max_length=128)
    run_type = models.IntegerField(default=1)
    risk = models.CharField(max_length=4)
    priority = models.IntegerField(default=1)
    file_name = models.CharField(max_length=128)
    category_id = models.IntegerField()
    description = models.TextField(blank=True)
    solution = models.TextField(blank=True)

    class Meta:
        db_table = "rule"

admin.site.register(Task)

