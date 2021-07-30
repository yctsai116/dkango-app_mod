from django.db import models


class SentRequests(models.Model):
    name = models.CharField(max_length=30)
    unit_code = models.CharField(max_length=50)
    customer_id = models.CharField(max_length=30)
    api_request = models.IntegerField()
    # api_content = models.CharField(max_length=50, null=True)
    notes = models.CharField(max_length=100, null=True)

    @property
    def is_success(self):
        return self.api_request == 200

    def serialize(self, **kwargs):
        return {
            "id": self.id,
            "name": self.name,
            "unit_code": self.unit_code,
            "customer_id": self.customer_id,
            "api_request": self.api_request,
            "notes": self.notes,
            **kwargs
        }
