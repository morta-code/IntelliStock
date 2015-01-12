from concurrent.futures import ThreadPoolExecutor
import time
import datetime

class Simulation:
    
    def __init__(self, application):
        self.application = application
        self.speed = -1
        self.interval = 0.1
        self.finish = False
        self.start_time = datetime.datetime.now()
        self.money = 0
        self.stocks = ()
        self.current_time = datetime.datetime.now()
    
    def set_start_time(self, start_time):
        """ Sets the start time of the simulation """
        self.start_time = start_time
        pass
    
    def set_speed(self, speed):
        """ Sets the speed of the simulation. Default (-1) is maximum speed (no game, just calculations)"""
        self.speed = speed
        pass

    def set_money(self, money):
        """ Sets the speed of the simulation. Default (-1) is maximum speed (no game, just calculations)"""
        self.money = money
        pass

    def do_simulation(self):
        """
        Executes on background thread
        """
        self.current_time = self.start_time
        while not self.finish:
            time.sleep(self.interval)
            self.current_time += self.speed*self.interval
            # TODO: main thread
            self.application.set_graph_times(self.start_time, self.current_time)

    def buy_stock(self, stock_name, amount):
        # TODO: thread safe
        self.money -= self.application.get_stock_price(stock_name, self.current_time)*amount
        self.stocks[stock_name] += amount

    def sell_stock(self, stock_name, amount):
        # TODO: thread safe
        self.buy_stock(stock_name, -amount)

    def simulation_done(self, future):
        self.application.receive_simulation_result(self, {})

    def start_simulation(self):
        """ Starts the simulation on a separate thread. Publishes back simulation results to the application """
        self.finish = False
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self.do_simulation)
        future.add_done_callback(self.simulation_done)

    def stop_simulation(self):
        self.finish = True