from realworld import utils


class StrReprMixin:
    """
    Mixin to provide a string representation of the model.
    This can be customized by setting the `strrepr_exclude_fields` attribute.
    """

    def __str__(self) -> str:
        extra_excludes = getattr(self, "strrepr_exclude_fields", [])
        return utils.class_str_repr(self, exclude_fields=extra_excludes)
