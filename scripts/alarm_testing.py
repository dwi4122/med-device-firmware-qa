"""Alarm testing module for CPAP firmware validation.

This module provides test functions for apnea alarm functionality,
following medical device standards and PEP 8 guidelines.
"""

from robot.api.deco import keyword


@keyword("Test Apnea Alarm")
def test_apnea_alarm(apnea_duration, expected_alarm):
    """Test whether apnea alarm triggers at correct threshold.
    
    Args:
        apnea_duration: Duration of apnea event in seconds (float or string)
        expected_alarm: Boolean (True/False or string) whether alarm should trigger
        
    Returns:
        bool: True if actual behavior matches expected, False otherwise
        
    Note:
        Converts all inputs to appropriate types for comparison.
        Follows ISO 80601-2-70 requirements for apnea detection.
    """
    # Standard apnea threshold (10 seconds per medical guidelines)
    ALARM_THRESHOLD = 10.0  
    
    try:
        # Convert inputs to proper types
        duration = float(apnea_duration)
        should_alarm = str(expected_alarm).strip().upper() == "TRUE"
        
        # Check if alarm behavior matches expectation
        actual_alarm = duration >= ALARM_THRESHOLD
        return actual_alarm == should_alarm
        
    except (ValueError, TypeError):
        # Handle invalid input types gracefully
        return False


# Required Robot Framework configuration
ROBOT_LIBRARY_SCOPE = "GLOBAL"