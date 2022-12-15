import json
import logging

import numpy as np
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from tensorflow.keras.datasets.mnist import load_data

from delta_x.module.tensorflow_saving.tasks import make_prediction

logger = logging.getLogger(__name__)


class IndexDashboardViews(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    login_url = reverse_lazy('dashboard:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.setdefault("view", self)
        # load MNIST dataset
        (_, _), (x_test, y_test) = load_data()
        # reshape data to have a single channel
        x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], x_test.shape[2], 1))
        # normalize pixel values
        x_test = x_test.astype('float32') / 255.0
        data = json.dumps({"signature_name": "serving_default", "instances": x_test[0:4].tolist()})
        headers = {"content-type": "application/json"}
        predictions = make_prediction.delay(data=data, headers=headers)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        for i, pred in enumerate(predictions.get(timeout=1)['predictions']):
            logger.info(f"True Value: {y_test[i]}, Predicted Value: {np.argmax(pred)}")
        return kwargs
