"""
Salary calculation logic for the real-time counter.
"""

from enum import Enum
from datetime import datetime
import time


class TimeFrame(Enum):
    """Enumeration for different salary timeframes."""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class SalaryCalculator:
    """Handles salary calculations and real-time counter logic."""
    
    # Constants for time conversions
    SECONDS_PER_MINUTE = 60
    MINUTES_PER_HOUR = 60
    HOURS_PER_DAY = 24
    DAYS_PER_WEEK = 7
    WEEKS_PER_MONTH = 4.33  # Average weeks per month
    MONTHS_PER_YEAR = 12
    
    def __init__(self, salary: float, timeframe: TimeFrame):
        """
        Initialize the salary calculator.
        
        Args:
            salary: The salary amount
            timeframe: The timeframe for the salary (hourly, daily, etc.)
        """
        self.salary = salary
        self.timeframe = timeframe
        self.start_time = None
        self.earnings_per_second = self._calculate_earnings_per_second()
    
    def _calculate_earnings_per_second(self) -> float:
        """Calculate earnings per second based on salary and timeframe."""
        if self.timeframe == TimeFrame.HOURLY:
            return self.salary / (self.MINUTES_PER_HOUR * self.SECONDS_PER_MINUTE)
        elif self.timeframe == TimeFrame.DAILY:
            return self.salary / (self.HOURS_PER_DAY * self.MINUTES_PER_HOUR * self.SECONDS_PER_MINUTE)
        elif self.timeframe == TimeFrame.WEEKLY:
            return self.salary / (self.DAYS_PER_WEEK * self.HOURS_PER_DAY * self.MINUTES_PER_HOUR * self.SECONDS_PER_MINUTE)
        elif self.timeframe == TimeFrame.MONTHLY:
            return self.salary / (self.WEEKS_PER_MONTH * self.DAYS_PER_WEEK * self.HOURS_PER_DAY * self.MINUTES_PER_HOUR * self.SECONDS_PER_MINUTE)
        elif self.timeframe == TimeFrame.YEARLY:
            return self.salary / (self.MONTHS_PER_YEAR * self.WEEKS_PER_MONTH * self.DAYS_PER_WEEK * self.HOURS_PER_DAY * self.MINUTES_PER_HOUR * self.SECONDS_PER_MINUTE)
        else:
            raise ValueError(f"Unsupported timeframe: {self.timeframe}")
    
    def start_counter(self):
        """Start the earnings counter."""
        self.start_time = time.time()
    
    def get_current_earnings(self) -> float:
        """
        Get the current earnings since the counter started.
        
        Returns:
            Current earnings as a float
        """
        if self.start_time is None:
            return 0.0
        
        elapsed_seconds = time.time() - self.start_time
        return elapsed_seconds * self.earnings_per_second
    
    def reset_counter(self):
        """Reset the earnings counter."""
        self.start_time = None
    
    def update_salary(self, salary: float, timeframe: TimeFrame):
        """
        Update salary and timeframe.
        
        Args:
            salary: New salary amount
            timeframe: New timeframe
        """
        self.salary = salary
        self.timeframe = timeframe
        self.earnings_per_second = self._calculate_earnings_per_second()
        # Reset counter when salary is updated
        self.reset_counter()
    
    @staticmethod
    def format_currency(amount: float, currency_symbol: str = "€") -> str:
        """
        Format amount as currency with 4 decimal places (showing 100ths of cents).
        
        Args:
            amount: Amount to format
            currency_symbol: Currency symbol to use
            
        Returns:
            Formatted currency string
        """
        # Format to 4 decimal places to show 100ths of cents
        return f"{currency_symbol}{amount:.4f}"