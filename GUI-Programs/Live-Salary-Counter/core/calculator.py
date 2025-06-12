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
        return self.salary_amount / Decimal(str(seconds_in_timeframe))
    
    def start(self):
        self.start_time = time.time()
        self.is_running = True

    def stop(self):
        self.is_running = False

    def reset(self):
        self.start_time = None
        self.is_running = False

    def get_current_earnings(self):
        if not self.is_running or self.start_time is None:
            return Decimal('0'), 0
        
        elapsed_time = time.time() - self.start_time
        current_earnings = self.earnings_per_second * Decimal(str(elapsed_time))

        return current_earnings, elapsed_time
    
    def format_currency(self, amount):
        # Round to 2 decimals
        rounded_amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return f"${rounded_amount:,.2f}"
    
    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
        
    def get_earnings_info(self):
        # Returns a dict

        current_earnings, elapsed_time = self.get_current_earnings()

        return {
            'current_earnings': current_earnings,
            'formatted_earnings': self.format_currency(current_earnings),
            'elapsed_time': elapsed_time,
            'formatted_time': self.format_time(elapsed_time),
            'earnings_per_second': self.earnings_per_second,
            'salary_amount': self.salary_amount,
            'time_frame': self.time_frame,
            'is_running': self.is_running
        }
    
    def get_projections(self):
        # Returns projections for different time periods
        projections = {}

        for period, seconds in self.time_multipliers.items():
            projected_earnings = self.earnings_per_second * Decimal(str(seconds))
            projections[period] = {
                'amount': projected_earnings,
                'formatted': self.format_currency(projected_earnings)
            }
        
        return projections


        
