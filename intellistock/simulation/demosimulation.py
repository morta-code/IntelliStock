# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 10:48:52 2014

@author: polpe
"""

from .simulation import Simulation

"""
OA: other approach
"""

class OASimulator:

    def set_do_simulation_callback(self, do_simulation):
        self.do_simulation = do_simulation

    def set_simulation_done_callback(self, simulation_done):
        self.simulation_done = simulation_done

    def start_simulation(self):
        """ Starts the simulation on a separate thread. Publishes back simulation results to the application """

        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self.do_simulation)
        future.add_done_callback(self.simulation_done)

        print ("simulation started")


class OASimulation:

    def __init__(self, application):
        self.application = application
        self.simulator = OASimulator()
    
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
        self.simulator.start_simulation()