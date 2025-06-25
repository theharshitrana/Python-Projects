import time
from playsound import playsound

def set_alarm():
    """Prompts user to set the alarm time."""
    while True:
        try:
            # Get the alarm hour and minute from the user
            hour = int(input("Enter the hour for the alarm (24-hour format): "))
            minute = int(input("Enter the minute for the alarm: "))

            # Validate the time input
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                print("❌ Invalid time input. Please enter a valid time in the 24-hour format.")
                continue
            else:
                return hour, minute
        except ValueError:
            print("❌ Invalid input. Please enter numbers for the time.")

def wait_for_alarm(alarm_hour, alarm_minute):
    """Waits until the alarm time is reached and plays a sound."""
    while True:
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min
        
        # Check if the current time matches the alarm time
        if current_hour == alarm_hour and current_minute == alarm_minute:
            print(f"⏰ It's {alarm_hour:02d}:{alarm_minute:02d}. Time to wake up! Alarm ringing...")
            playsound('alarm_sound.mp3')  # Replace with your own alarm sound file path
            break
        else:
            # Wait and keep checking
            print(f"Current Time: {time.strftime('%H:%M:%S')} - Waiting for alarm...")
            time.sleep(30)  # Check every 30 seconds

def main():
    print("Welcome to the Simple Alarm Clock!")
    
    while True:
        # Set the alarm
        alarm_hour, alarm_minute = set_alarm()
        print(f"Alarm set for {alarm_hour:02d}:{alarm_minute:02d}.")
        
        # Wait for the alarm and play the sound when it's time
        wait_for_alarm(alarm_hour, alarm_minute)
        
        # Ask if the user wants to set another alarm
        repeat = input
