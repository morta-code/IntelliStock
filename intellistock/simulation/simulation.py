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
        self.stocks = {}
        self.current_time = datetime.datetime.now()
        self.interest = 0.003 #Kötési díj
    
    def set_start_time(self, start_time):
        """ Sets the start time of the simulation """
        self.start_time = start_time
        pass
    
    def set_speed(self, speed):
        """ Sets the speed of the simulation. Default (-1) is maximum speed (no game, just calculations)"""
        self.speed = speed
        pass

    def set_money(self, money):
        """ Sets the starting money of the simulation"""
        self.money = money
        pass

    def set_interest(self, interest):
        """ Sets the interest of a transaction"""
        self.interest = interest
        pass

    def do_simulation(self):
        """
        Executes on background thread
        """
        print("Starting simulation")
        self.current_time = self.start_time
        while not self.finish:
            print("Simulation step " + str(self.current_time))
            time.sleep(self.interval)
            self.current_time += self.speed*datetime.timedelta(0,self.interval)
            self.application.lock.acquire()
            try:
                self.application.set_graph_times(self.start_time, self.current_time)
            finally:
                self.application.lock.release()

    def buy_stock(self, stock_name, amount):
        price = self.application.get_stock_price(stock_name, self.current_time)*amount
        self.money -= price + abs(price) * self.interest
        if stock_name in self.stocks:
            self.stocks[stock_name] += amount
        else:
            self.stocks[stock_name] = amount
        self.application.lock.acquire()
        try:
            self.update_stock_list()
        finally:
            self.application.lock.release()

    def update_stock_list(self):
        self.application.lock.acquire()
        try:
            self.application.set_my_stocks(self.stocks)
        finally:
            self.application.lock.release()

    def sell_stock(self, stock_name, amount):
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