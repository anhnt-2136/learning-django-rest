from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class CustomResponseMixin(ModelViewSet):
    """
    Mixin to format all responses with {data: ...} structure
    """

    def response(self, data=None, status=None):
        if data is None:
            data = []
        return Response({"data": data}, status=status)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return self.response(response.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self.response(response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return self.response(response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return self.response(response.data)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return self.response(response.data)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return self.response(response.data)
