# DRF Field level update permission mixin
Generic mixin for creating field level permissions in Django rest framework.

For instance, consider the case where there is a `VacationRequest` model that has the fields `start_date`/`end_date` and `approved_by_manager`, where the fields are updated by `Employee` and `Manager` respectively. 


### Use
1. Add `FieldLevelUpdatePermissionsMixin` to the serializer
2. Implement `has_write_permission(
        self, request: td.Request, instance: VacationRequest, field: str
    ) -> bool`
    
### Example
```
class VacationRequestSerializer(
    FieldLevelUpdatePermissionsMixin,
    serializers.ModelSerializer
):
    def has_write_permission(
        self, request: td.Request, instance: VacationRequest, field: str
    ) -> bool:
        if field in ["start_date", "end_date"]:
            return instance.owner == request.user
        if field == "approved_by_manager":
            return instance.owner.profile.reports_to == request.user
        return False
```
