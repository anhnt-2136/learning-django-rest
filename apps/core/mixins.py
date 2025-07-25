from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from realworld import utils


class StrReprMixin:
    """
    Mixin to provide a string representation of the model.
    This can be customized by setting the `strrepr_exclude_fields` attribute.
    """

    def __str__(self) -> str:
        extra_excludes = getattr(self, "strrepr_exclude_fields", [])
        return utils.class_str_repr(self, exclude_fields=extra_excludes)


class BaseResponseMixin:
    """
    Base mixin that provides the common response formatting method.
    Use this along with specific operation mixins.
    """

    def response(self, data=None, status=None, wrapped=True):
        if data is None:
            data = []
        if wrapped is False:
            return Response(data, status=status)

        return Response({"data": data}, status=status)


class CustomListMixin(BaseResponseMixin, mixins.ListModelMixin):
    """
    Mixin to format list responses with {data: ...} structure.
    Must be used with BaseResponseMixin and a ViewSet that has list() method.
    """

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return self.response(response.data)


class CustomCreateMixin(BaseResponseMixin, mixins.CreateModelMixin):
    """
    Mixin to format create responses with {data: ...} structure.
    Must be used with BaseResponseMixin and a ViewSet that has create() method.
    """

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self.response(response.data)


class CustomRetrieveMixin(BaseResponseMixin, mixins.RetrieveModelMixin):
    """
    Mixin to format retrieve responses with {data: ...} structure.
    Must be used with BaseResponseMixin and a ViewSet that has retrieve()
    method.
    """

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return self.response(response.data)


class CustomUpdateMixin(BaseResponseMixin, mixins.UpdateModelMixin):
    """
    Mixin to format update responses with {data: ...} structure.
    Must be used with BaseResponseMixin and a ViewSet that has update() method.
    """

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return self.response(response.data)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return self.response(response.data, wrapped=False)


class CustomDestroyMixin(BaseResponseMixin, mixins.DestroyModelMixin):
    """
    Mixin to format destroy responses with {data: ...} structure.
    Must be used with BaseResponseMixin and a ViewSet that has destroy() method.
    """

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return self.response(response.data)


# For backward compatibility - includes all CRUD operations
class CustomModelViewSet(
    CustomListMixin,
    CustomCreateMixin,
    CustomRetrieveMixin,
    CustomUpdateMixin,
    CustomDestroyMixin,
    GenericViewSet,
):
    """
    Complete mixin that formats all CRUD responses with {data: ...} structure.
    This is kept for backward compatibility.
    """

    pass


class CustomReadOnlyModelViewSet(
    CustomListMixin,
    CustomRetrieveMixin,
    GenericViewSet,
):
    """
    Mixin to format read-only responses with {data: ...} structure.
    This is useful for ViewSets that only support list and retrieve operations.
    """

    pass
