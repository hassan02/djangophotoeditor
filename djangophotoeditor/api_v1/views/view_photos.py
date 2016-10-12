import os

from api_v1.filters import ImageEditor
from api_v1.permissions import IsPhotoFolderOwner, IsPhotoOwner
from api_v1.serializers import PhotoSerializer
from django.shortcuts import get_object_or_404
from djangophotoeditor.settings import MEDIA_ROOT
from photos.models import Folder, Photo
from rest_framework.exceptions import ParseError
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated


class PhotoView(ListCreateAPIView):
    """
    Get all photos, or create a new photo without folder.
    """
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """
        Overrides the default perform_create method
        Save image uploader as current user
        """

        image = self.request.FILES.get('image')
        if not image:
            raise ParseError(detail="Please upload a valid image")

        serializer.save(uploader=self.request.user, folder=None)

    def get_queryset(self):
        """Returns all photos for a particular user only"""
        return Photo.objects.filter(uploader=self.request.user)


class FolderPhotoView(CreateAPIView):
    """
    Create a new photo in a folder.
    """
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticated, IsPhotoFolderOwner, )

    def perform_create(self, serializer):
        """
        Overrides the default perform_create method
        Save image uploader as current user and folder as current folder
        """
        folder_id = self.kwargs.get('pk')
        folder = get_object_or_404(Folder, pk=folder_id)
        """
        Overrides the default perform_create method
        Save current user as image uploader
        """
        image = self.request.FILES.get('image')
        if not image:
            raise ParseError(detail="Please upload a valid image")
        serializer.save(uploader=self.request.user, folder=folder)


class PhotoDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update or delete a photo
    """
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    permission_classes = (IsAuthenticated, IsPhotoOwner)

    def perform_destroy(self, instance):
        """Delete image instance"""
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)
        if instance.edited_image:
            edited_image_path = os.path.join(
                MEDIA_ROOT, instance.edited_image)
            if os.path.exists(edited_image_path):
                os.remove(edited_image_path)
        instance.delete()

    def perform_update(self, serializer):
        """Performs image update by applying filters"""
        photo_id = self.kwargs.get('pk')
        photo = Photo.objects.filter(
            pk=photo_id,
            uploader=self.request.user).first()
        image = photo.image

        filters = self.request.data.get('filters', '')
        edited_image = ImageEditor(image, filters).apply_filters()

        filename, file_format = os.path.splitext(image.name)
        edited_image_url = '{}_edited{}'.format(filename, file_format)
        edited_image_path = '{}/{}'.format(
            MEDIA_ROOT, edited_image_url)
        edited_image.save(edited_image_path)

        instance = serializer.save()
        instance.title = serializer.validated_data.get('title')
        instance.edited_image = edited_image_url
        if self.request.data.get('save'):
            edited_image.save('{}/{}'.format(MEDIA_ROOT, image.name))
            instance.save()
