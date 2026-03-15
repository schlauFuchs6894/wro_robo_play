from buildhat import Motor
import time

# Initialize motor on port A
m = Motor('A')

print("Starting motor...")
# Start motor
m.start(50) # Speed
time.sleep(2)

print("Stopping motor...")
# Stop motor
m.stop()
time.sleep(2)

# Run for specific angle
print("Running 360 degrees...")
m.run_for_degrees(360, 100)
m.run_to_position(0,50)