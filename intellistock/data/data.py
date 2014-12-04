# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 14:23:08 2014

@author: wondercsabo
"""

class DataManager:
    """Entry point for access all data related methods. Singleton."""
    
    def getTrades(begin, end):
        """Returns the trades between dates begin and end."""
        
    def getStocks():
        """Returns the stocks currently stored in the database."""

    def startPolling():
        """Starts the polling of the BSE page for new data."""
        
    def stopPolling():
        """Stops polling of the BSE page."""
        
    def updateStocks():
        """This will call the mediator to update the gui with new data."""

