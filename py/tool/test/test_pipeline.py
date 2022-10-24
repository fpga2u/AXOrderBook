# -*- coding: utf-8 -*-

from ast import Lambda
from tool.test_util import *

from tool.pipeline import *




def test_pipeline_I1E1():
    '''
    loader -> process -> saver
    '''
    class PPStageI1E1_loader(PPStageI1E1):
        def __init__(self, queue_size):
            super(PPStageI1E1_loader, self).__init__(self.main, queue_size=queue_size, f_prev_stage_stopped=None)

        def main(self):
            for i in range(10):
                self.output(i, 0.1)
            self.done = True

            
    class PPStageI1E1_process(PPStageI1E1):
        def __init__(self, prev_stage, queue_size):
            super(PPStageI1E1_process, self).__init__(self.main, queue_size=queue_size, f_prev_stage_stopped=prev_stage.stopped)
            self.prev_stage = prev_stage

        def main(self):
            while True:
                try:
                    data = self.prev_stage.read(1)
                except Exception as e:  # TODO: ugly
                    print(f'process read data raise:{e}')
                    break
                self.output(data*20+1, 0.1)
            self.done = True


    class PPStageI1E1_save(PPStageI1E1):
        def __init__(self, prev_stage):
            super(PPStageI1E1_save, self).__init__(self.main, f_prev_stage_stopped=prev_stage.stopped)
            self.prev_stage = prev_stage

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
            self.done = True

    s1 = PPStageI1E1_loader(queue_size=20)
    s2 = PPStageI1E1_process(prev_stage=s1, queue_size=20)
    s3 = PPStageI1E1_save(prev_stage=s2)

    s3.start()
    s2.start()
    s1.start()

    s1.wait_for_stop(0.1)
    s2.wait_for_stop(0.1)
    s3.wait_for_stop(0.1)


def test_pipeline_id():
    #         
    #        /-> process1 -\
    #       /    ^   |      \
    #      /     |   V       \
    #load ----> process2 -----> save
    #      \     ^   |       /
    #       \    |   V      / 
    #        \-> process3 -/
    #
    '''
    '''
    STEP = 1
    class PPStage_load(PPStage):
        def __init__(self, output_queue=[], output_list=[]):
            super(PPStage_load, self).__init__(main_func=self.main, f_prev_stage_stopped=None)
            self.output_queue = output_queue
            self.output_list = output_list

        def output_pop_over(self):
            all_over = 0
            for Q in self.output_queue:
                all_over += Q.empty()
            return all_over == len(self.output_queue)

        def main(self):
            for i in self.output_list:
                for Q in self.output_queue:
                    Q.put(i)
                time.sleep(STEP)
            for i in range(len(self.output_queue)):
                self.output_queue[i].put(-1)    #finish
            self.done = True
        

    class PPStage_process(PPStage):
        def __init__(self, prev_stage, process_id, current_id_queue, to_saver_queue, coeval_queue:map, to_coeval_queues:list):
            super(PPStage_process, self).__init__(main_func=self.main, f_prev_stage_stopped=prev_stage.stopped)
            self.ID = process_id
            self.current_id_queue = current_id_queue
            self.to_saver_queue = to_saver_queue
            self.coeval_queue = coeval_queue
            self.to_coeval_queues = to_coeval_queues
            self.err_nb = 0

        def output_pop_over(self):
            return self.to_saver_queue.empty()

        def main(self):
            i = 0
            while True:
                try:
                    current_worker_id = self.current_id_queue.get(timeout=STEP*2)
                    print(f'Processor-{self.ID} get #{i} current_worker_id={current_worker_id}. ')
                    if current_worker_id < 0:   #finish
                        self.to_saver_queue.put(-self.ID)   #I'm finished.
                        break
                    elif current_worker_id==self.ID:
                        print(f'Processor-{self.ID} put #{i} data to server. ')
                        self.to_saver_queue.put(self.ID*self.ID)
                        time.sleep(STEP)

                        for Q in self.to_coeval_queues: #I work over.
                            Q.put(self.ID)
                    else:
                        try:
                            coeval_data = self.coeval_queue[current_worker_id].get(timeout=STEP*3)
                            print(f'Processor-{self.ID} get coeval_data from {current_worker_id}={coeval_data}. ')
                        except Exception as e:
                            self.err_nb += 1
                            print(f'ERROR: Processor-{self.ID} get coeval_data from {current_worker_id} raise:{e}. ')
                except Exception as e:
                    self.err_nb += 1
                    print(f'ERROR: Processor-{self.ID} read data raise:{e}. ')
                    break
                i += 1
            print(f'Processor-{self.ID} done. ')
            self.done = True
            
        # callback for next pipe-stage to dequeue data
        def read(self, timeout):
            return self.output_queue.get(timeout=timeout)

    class PPStage_save(PPStage):
        def __init__(self, current_id_queue, prev_stages:list, input_queue:list):
            def all_stopped():
                return sum([x.stopped() for x in prev_stages])==len(prev_stages)
            super(PPStage_save, self).__init__(main_func=self.main, f_prev_stage_stopped=all_stopped)
            self.current_id_queue = current_id_queue
            self.input_queue = input_queue
            self.captured = []
            self.err_nb = 0
    
        def main(self):
            i = 0
            done_list = [0] * len(self.input_queue)
            while True:
                try:
                    current_worker_id = self.current_id_queue.get(STEP)
                    print(f'saver get #{i} current_worker_id={current_worker_id}. ')

                    if current_worker_id<0:
                        for Q in self.input_queue:
                            data = Q.get(STEP)
                            print(f'saver get #{i} finish={data}. ')
                        break
                    else:
                        data = self.input_queue[current_worker_id].get(STEP)
                        print(f'saver get #{i} data={data}. ')
                        if data < 0:
                            done_list[-data] = 1
                        else:
                            assert data==current_worker_id*current_worker_id, f"check worker data fail"
                            self.captured.append(current_worker_id)
                except Exception as e:
                    self.err_nb += 1
                    print(f'ERROR: saver read #{i} data raise:{e}. ')
                    break
                i += 1
                if sum(done_list) == len(self.input_queue):
                    break
            self.done = True

        # override
        def output_pop_over(self):
            return True
    ##
    current_id_queue = []
    for _ in range(3+1):
        current_id_queue.append(queue.Queue(1))

    process_coeval_queue = []
    for i in range(3):
        to_coeval_queue = {}
        for j in range(3):
            if i!=j:
                to_coeval_queue[j] = queue.Queue(1)
        process_coeval_queue.append(to_coeval_queue)

    processed_data_queue = []
    for _ in range(3):
        processed_data_queue.append(queue.Queue(1))

    work_flow = [0, 1, 2]
    loader = PPStage_load(current_id_queue, output_list=work_flow)
    p0 = PPStage_process(loader, 0, current_id_queue[0], processed_data_queue[0], process_coeval_queue[0], [process_coeval_queue[1][0], process_coeval_queue[2][0]])
    p1 = PPStage_process(loader, 1, current_id_queue[1], processed_data_queue[1], process_coeval_queue[1], [process_coeval_queue[0][1], process_coeval_queue[2][1]])
    p2 = PPStage_process(loader, 2, current_id_queue[2], processed_data_queue[2], process_coeval_queue[2], [process_coeval_queue[0][2], process_coeval_queue[1][2]])
    saver = PPStage_save(current_id_queue[-1], [p0, p1, p2], processed_data_queue)

    saver.start()
    p0.start()
    p1.start()
    p2.start()
    loader.start()

    saver.wait_for_stop(0.1)
    p0.wait_for_stop(0.1)
    p1.wait_for_stop(0.1)
    p2.wait_for_stop(0.1)
    loader.wait_for_stop(0.1)

    err_nb = p0.err_nb + p1.err_nb + p2.err_nb + saver.err_nb

    if work_flow==saver.captured and err_nb==0:
        print("test_pipeline_id PASS")
    else:
        print("test_pipeline_id FAIL")
