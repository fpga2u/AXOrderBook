# -*- coding: utf-8 -*-

from tool.test_util import *

from tool.pipeline import *




def test_pipeline_I1E1():
    class PPStageI1E1_loader(PPStageI1E1):
        def __init__(self, queue_size):
            super(PPStageI1E1_loader, self).__init__(self.main, queue_size=queue_size, prev_stage=None)

        def main(self):
            for i in range(10):
                self.output(i, 0.1)
            self.stopped = True

            
    class PPStageI1E1_process(PPStageI1E1):
        def __init__(self, prev_stage, queue_size):
            super(PPStageI1E1_process, self).__init__(self.main, queue_size=queue_size, prev_stage=prev_stage)

        def main(self):
            while True:
                try:
                    data = self.prev_stage.read(1)
                except Exception as e:  # TODO: ugly
                    print(f'process read data raise:{e}')
                    break
                self.output(data*20+1, 0.1)
            self.stopped = True

    class PPStageI1E1_save(PPStageI1E1):
        def __init__(self, prev_stage):
            super(PPStageI1E1_save, self).__init__(self.main, prev_stage=prev_stage)

        def main(self):
            i = 0
            while True:
                try:
                    data = self.prev_stage.read(1)
                    print(f'save data:{data}')
                except Exception as e:  # TODO: ugly
                    print(f'save read data raise:{e}')
                    break
                assert data==i*20+1, f'check save data error golden={i*20+1}, data={data}'
                i += 1
            self.stopped = True

    s1 = PPStageI1E1_loader(queue_size=20)
    s2 = PPStageI1E1_process(prev_stage=s1, queue_size=20)
    s3 = PPStageI1E1_save(prev_stage=s2)

    s3.start()
    s2.start()
    s1.start()

    s1.wait_for_stop(0.1)
    s2.wait_for_stop(0.1)
    s3.wait_for_stop(0.1)
