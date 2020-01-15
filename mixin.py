from rest_framework.exceptions import ValidationError

import type_declarations as td


class FieldLevelUpdatePermissionsMixin:
    """
    Field level permissions for updates. To use, add mixin to Serializer and
    implement `has_write_permission()`
    """

    permission_fields: list

    def __init_subclass__(*a, **kw):
        derived_cls = a[0]
        if "has_write_permission" not in dir(derived_cls):
            raise NotImplementedError(
                f"Classes extending {__class__} must"
                f" implement has_write_permission"
            )

    def has_write_permission(self, request, instance, field) -> bool:
        pass

    def update(self, instance: td.Model, validated_data: dict) -> td.Model:
        request = self.context["request"]
        self._check_field_permissions(request, validated_data, instance)
        return super().update(instance, validated_data)

    def _check_field_permissions(self, request, validated_data, instance):
        fields_intersect = set(self.permission_fields).intersection(
            validated_data.keys()
        )
        for field in fields_intersect:
            if not self.has_write_permission(request, instance, field):
                raise ValidationError(
                    f"Authenticated user {request.user.email} does"
                    f" not have update permissions for the field "
                    f"{field}"
                )
