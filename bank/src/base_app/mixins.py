from rest_framework import mixins, status
from rest_framework.response import Response


class CustomCreateModelMixin(mixins.CreateModelMixin):
    '''Extended CreateModelMixin with determined class field `custom_serializer` to extend
    this serializer with additional fields and validate them.
    Setting new serializer is in method `perform_create`.
    '''

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        self.custom_serializer = serializer
        self.custom_serializer.is_valid(raise_exception=True)
        self.perform_create(self.custom_serializer)
        headers = self.get_success_headers(self.custom_serializer.data)
        return Response(self.custom_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
