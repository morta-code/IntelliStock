from concurrent.futures import ThreadPoolExecutor
import time


class Simulation:
    
    def __init__(self, application):
        self.application = application
    
    def set_start_time(self, start_time):
        """ Sets the start time of the simulation """
        pass
    
    def set_speed(self, speed):
        """ Sets the speed of the simulation. Default is maximum speed (no game)"""
        pass

    def do_simulation(self):
        """
        Executes on background thread
        """
        time.sleep(10)

    def simulation_done(self, future):
        self.application.receive_simulation_result(self, {})

    def start_simulation(self):
        """ Starts the simulation on a separate thread. Publishes back simulation results to the application """

        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self.do_simulation)
        future.add_done_callback(self.simulation_done)

    pass