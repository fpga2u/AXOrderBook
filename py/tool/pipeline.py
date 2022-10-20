# -*- coding: utf-8 -*-
import abc

import sys
import time
import threading


# import the Queue class from Python 3
if sys.version_info >= (3, 0):
    import queue
# otherwise, import the Queue class for Python 2.7
else:
    import Queue as queue


class PPStage(metaclass=abc.ABCMeta):
    def __init__(self, main_func, prev_stage=None):
        self.main_func = main_func
        self.stopped = False
        self.t = None
        self.prev_stage = prev_stage

    # NEED to be override
    @abc.abstractmethod
    def output_pop_over(self):
        return None

    def start(self):
        self.t = threading.Thread(target=self.main_func, args=())
        self.t.daemon = True
        self.t.start()

    # callback for main() to stop
    def wait_for_stop(self, time_step):
        if self.prev_stage is not None:
            while not self.prev_stage.stopped:
                time.sleep(time_step)
        assert self.output_pop_over() is not None, "Not Implement output_pop_over()"
        while not self.output_pop_over():
            time.sleep(time_step)


class PPStageI1E1(PPStage):
    def __init__(self, main_func, prev_stage=None, queue_size=None):
        super(PPStageI1E1, self).__init__(main_func, prev_stage)
        # initialize the queue used to store data
        if queue_size is not None:
            self.Q = queue.Queue(maxsize=queue_size)
        else:
            self.Q = None

    # enqueue API to output data to next pipe-stage
    def output(self, data, time_step):
        while self.Q.full():
            time.sleep(time_step)
        self.Q.put(data)

    # callback for next pipe-stage to dequeue data
    def read(self, timeout):
        return self.Q.get(timeout=timeout)

    # override
    def output_pop_over(self):
        if self.Q is not None:
            return self.Q.empty()
        else:
            return True


