import numpy as np
import logging

class EarlyStopping:
    """Stop the training process in advance.

    Parameters
    ----------
    monitor: Objects monitored by the monitor, here is 'acc' and 'loss'
    min_delta: The tolerance of abnormal results is considered as normal
    when the results change within the range of amplitude
    patience: Number of epochs with no improvement after which training
    will be stopped.
    mode: One of `{"min", "max"}`. "min" corresponds to "loss","max" corresponds
    to "acc"
    """
    def __init__(self,
               monitor='loss',
               min_delta=0,
               patience=0,
               mode='min'):
        super(EarlyStopping, self).__init__()

        self.monitor = monitor
        self.patience = patience
        self.min_delta = abs(min_delta)

        self.wait = 0
        self.stopped_epoch = 0
        self.best = np.Inf if self.monitor_op == np.less else -np.Inf
        self.best_weights = None
        self.best_epoch = 0

        if mode not in ['min', 'max']:
            logging.warning('EarlyStopping mode %s is unknown', mode)

        if mode == 'min':
          self.monitor_op = np.less
        elif mode == 'max':
          self.monitor_op = np.greater
        else:
          if (self.monitor.endswith('acc') or self.monitor.endswith('accuracy')):
            self.monitor_op = np.greater
          else:
            self.monitor_op = np.less

        if self.monitor_op == np.greater:
          self.min_delta *= 1
        else:
          self.min_delta *= -1

    def __call__(self, epoch, logs=None):
        current = self.get_monitor_value(logs)
        if current is None:
          return
        if self.best_weights is None:
            # Restore the weights after first epoch if no progress is ever made.
            self.best_weights = self.model.parameters()

        if self._is_improvement(current, self.best):
            self.best = current
            self.best_epoch = epoch
            self.best_weights = self.model.parameters()
        else:
            self.wait += 1
            if self.wait >= self.patience:
                self.stopped_epoch = self.best_epoch + self.wait
        return self.best_epoch, self.stopped_epoch

    def get_monitor_value(self, mm_logs):
        """Get the monitor value from mm framework on each epoch.Maybe the monitor
        valude includes one of "acc" and "loss".
        Parameters
        ----------
        logs:logs from mm framework when training.
        -------
        """
        monitor_value = self._get_value(mm_logs)
        if monitor_value is None:
            logging.warning('Early stopping conditioned on metric `%s` ',
                          self.monitor)
        return monitor_value

    def _is_improvement(self, monitor_value, reference_value):
        return self.monitor_op(monitor_value - self.min_delta, reference_value)

    def _get_value(self, mm_logs):
