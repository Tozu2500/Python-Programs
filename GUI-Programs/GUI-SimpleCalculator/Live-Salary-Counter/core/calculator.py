# This module handles salary-related calculations

import time
from decimal import Decimal, ROUND_HALF_UP

class SalaryCalculator:
    
    def __init__(self, salary_amount, time_frame, time_multipliers):

        """
        # Initialize the calc
        Args:
            salary_amount (float): The salary amount
            time_frame (str): Time frame (hour, day, week, month, year)
            time_multipliers (dict): Dictionary of time frame multipliers
        """
    
        self.salary_amount = Decimal(str(salary_amount))
        self.time_frame
        self.time_multipliers = time_multipliers
        self.start_time = None
        self.is_running = False

        # Earning per second calculations
        self.earnings_per_second = self._calculate_earnings_per_second()

    def _calculate_earnings_per_second(self):
        seconds_in_timeframe = self.time_multipliers[self.time_frame]
        
        
