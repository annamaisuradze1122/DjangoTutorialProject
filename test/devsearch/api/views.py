from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project

from api import serializers

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'GET':'/api/projects/id/vote'},
    ]
    return Response(routes)


@api_view(['GET'])
def getProjects(request):
    project = Project.objects.all()
    serializers = ProjectSerializer(project, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.filter(id=pk)
    serializers = ProjectSerializer(project, many=True)
    return Response(serializers.data)

