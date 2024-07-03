import graphene
from graphene_django.types import DjangoObjectType

from .models import Application, CandidateProfile


class CandidateProfileType(DjangoObjectType):
    class Meta:
        model = CandidateProfile
        fields = ('id', 'name', 'last_name', 'education', 'experience')

class Query(graphene.ObjectType):
    all_profiles = graphene.List(CandidateProfileType)

    def resolve_all_profiles(self, info):
        return CandidateProfile.objects.all()

schema = graphene.Schema(query=Query)




