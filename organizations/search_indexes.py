import datetime
from django.db import models

from haystack import indexes
from .models import Organization, Project, ApplicationScope


class OrganizationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    activity_description = indexes.CharField(model_attr='activity_description')
    inserted_by = indexes.CharField(model_attr='inserted_by')
    inserted_at = indexes.DateTimeField(model_attr='inserted_at')

    def get_model(self):
        return Organization

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            inserted_at__lte=datetime.datetime.now())

    def prepare_countries(self, obj):
        return [c.name for c in obj.countries_set.all()]


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    organization = indexes.CharField(model_attr='organization')
    application_scope = indexes.CharField(model_attr='application_scope')
    description = indexes.CharField(model_attr='description')
    inserted_by = indexes.CharField(model_attr='inserted_by')
    inserted_at = indexes.DateTimeField(model_attr='inserted_at')

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            inserted_at__lte=datetime.datetime.now())
