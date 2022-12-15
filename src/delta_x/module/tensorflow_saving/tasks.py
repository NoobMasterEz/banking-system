import json

import requests
from django.conf import settings

from delta_x.schedule_task.celery import app


@app.task(serializer='json', name='other_task')
def make_prediction(data, headers):
    json_response = requests.post(settings.TF_SAVING_URL, data=data, headers=headers)
    predictions = json.loads(json_response.text)
    return predictions
