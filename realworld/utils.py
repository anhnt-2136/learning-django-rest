def class_str_repr(instance, exclude_fields=None):
    """
    Helper function to create string representation using all model fields
    """
    if exclude_fields is None:
        exclude_fields = []

    class_name = instance.__class__.__name__
    field_pairs = []

    # Get all class fields
    for field in instance._meta.fields:
        field_name = field.name
        if field_name not in exclude_fields:
            value = getattr(instance, field_name, None)
            field_pairs.append(f"{field_name}={value}")

    return f"{class_name}({', '.join(field_pairs)})"
