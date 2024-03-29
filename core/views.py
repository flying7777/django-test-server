from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import NoteSerializer
from .models import Notes

def front(request):
    context = { }
    return render(request, "index.html", context)

@api_view(['GET', 'POST'])
def note(request):

    if request.method == "GET":
        note = Notes.objects.all()
        serializer = NoteSerializer(note, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            note = Notes.objects.all()
            _serializer = NoteSerializer(note, many=True)
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["DELETE", "PUT"])
def note_detail(request, pk):
    try:
        note = Notes.objects.get(id=pk)
        if request.method == "PUT":
            serializer = NoteSerializer(instance=note, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_205_RESET_CONTENT)
        if request.method == "DELETE":
            note.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    except Notes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    