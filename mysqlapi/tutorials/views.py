from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerializer
from rest_framework.decorators import api_view


@api_view(["GET", "POST", "DELETE"])
def tutorials_list(request):
    # CREATE TUTORAIL
    if request.method == "POST":
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(
                tutorial_serializer.data, status=status.HTTP_201_CREATED
            )
        print("******")
        print(request)
        print("******")
        return JsonResponse(
            tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    # GET ALL TUTORIAL
    elif request.method == "GET":
        tutorials = Tutorial.objects.all()

        title = request.GET.get("title", None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)

        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)

    # DELETE ALL TUTORIAL
    elif request.method == "DELETE":
        count = Tutorial.objects.all().delete()
        return JsonResponse(
            {"message": "Tutorials were deleted successfully".format(count[0])},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET", "PUT", "DELETE"])
def tutorial_details(request, pk):
    tutorial = Tutorial.objects.get(pk=pk)

    # GET ONE TUTORIAL
    if request.method == "GET":
        tutorials_serializer = TutorialSerializer(tutorial)
        return JsonResponse(tutorials_serializer.data)

    # UPDATE TUTORIAL
    elif request.method == "PUT":
        tutorial_data = JSONParser().parse(request)
        tutorials_serializer = TutorialSerializer(tutorial, data=tutorial_data)
        if tutorials_serializer.is_valid():
            tutorials_serializer.save()
            return JsonResponse(tutorials_serializer.data)
        return JsonResponse(tutorials_serializer.errors, status=status.HTTP_400_REQUEST)

    # DELETE TUTORIAL
    if request.method == "DELETE":
        tutorial.delete()
        return JsonResponse(
            {"message": "Tutorial was deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


# GEt all published tutorials
@api_view(["GET"])
def tutorials_list_published(request):
    if request.method == "GET":
        tutorial = Tutorial.objects.filter(published=True)
        tutorials_serializer = TutorialSerializer(tutorial, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)