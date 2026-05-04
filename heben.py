"""Test motors"""
import time
from robo_init import robo, setup, create_motor_pair, ready_wait_for_start, stop_all
# from buildhat import Hat, Motor, MotorPair,ColorDistanceSensor,ColorSensor, Light, DistanceSensor
# from buildhat.devices import Device
# from buildhat.exc import DeviceError, MotorError
from turtle import color
from gpiozero import Button
from signal import pause
import time

FULL_OPEN_POS = 128
CLOSED_POS = -15
OPEN_POS = CLOSED_POS + -75
TURM_HALTE_POS = CLOSED_POS + -33
ARTEFAKT_HALTE_POS = TURM_HALTE_POS
BESUCHER_HALTE_POS = CLOSED_POS + -10

POS_MAX_OBEN = -60
POS_MAX_UNTEN = -170
#Lift Top:(soll100 ist-60), -1170
#Lift unten:(soll60 ist-170), -220
POS_TOP_BOTTOM = 950
ROTATIONS_TOP_BOTTOM = POS_TOP_BOTTOM / 360
POS_TURM_ABGESTELLT_UNTEN = POS_MAX_UNTEN -170
POS_TURM_ABGESTELLT_OBEN = POS_MAX_UNTEN -700
POS_TURM_ANGEHOBEN = POS_MAX_UNTEN -220
POS_TURM_STAPELN = POS_MAX_UNTEN -850
POS_ARTEFAKT_ABGESTELLT = POS_MAX_UNTEN -150
POS_ARTEFAKT_ANGEHOBEN = POS_MAX_UNTEN -180
POS_BESUCHER_ABGESTELLT = POS_MAX_UNTEN -155
POS_BESUCHER_ANGEHOBEN = POS_MAX_UNTEN -185

def calibrieren_gabel():
    print("GABEL CALIBRIEREN!")
    print("to full open postin!")
    robo.gabel.plimit(0.8)
    robo.gabel.run_to_position(FULL_OPEN_POS, 4, direction='anticlockwise')
    gabel_apos= robo.gabel.get_aposition()
    gabel_pos= robo.gabel.get_position()
    print(f"Gabel:(soll{FULL_OPEN_POS} ist{gabel_apos}), {gabel_pos}")

    print("to closed postin!")
    ready_wait_for_start()
    robo.gabel.plimit(0.8)
    robo.gabel.run_to_position(CLOSED_POS, 4, direction='clockwise')
    gabel_apos= robo.gabel.get_aposition()
    gabel_pos= robo.gabel.get_position()
    print(f"Gabel:(soll{CLOSED_POS} ist{gabel_apos}), {gabel_pos}")

def calibrieren_lift():
    print("to top postin!")
    ready_wait_for_start()
    robo.lift.plimit(0.57)
    robo.lift.run_for_rotations(-ROTATIONS_TOP_BOTTOM*1.2) #1.2 factor for upward.
    #robo.lift.run_to_position(POS_MAX_OBEN, 4, direction='anticlockwise')
    lift_apos= robo.lift.get_aposition()
    lift_pos= robo.lift.get_position()
    print(f"Lift Top:(soll{POS_MAX_OBEN} ist{lift_apos}), {lift_pos}")

    print("LIFT CALIBRIEREN!")
    print("to lowest postion!")
    ready_wait_for_start()
    lift_apos= robo.lift.get_aposition()
    lift_pos= robo.lift.get_position()
    print(f"Lift Top:(soll{POS_MAX_OBEN} ist{lift_apos}), {lift_pos}")
    robo.lift.plimit(0.6)
    robo.lift.run_for_rotations(ROTATIONS_TOP_BOTTOM)
    robo.lift.run_to_position(POS_MAX_UNTEN, 4, direction='clockwise')
    lift_apos= robo.lift.get_aposition()
    lift_pos= robo.lift.get_position()
    print(f"Lift unten:(soll{POS_MAX_UNTEN} ist{lift_apos}), {lift_pos}")
    ready_wait_for_start()
    lift_apos= robo.lift.get_aposition()
    lift_pos= robo.lift.get_position()
    print(f"Lift unten:(soll{POS_MAX_UNTEN} ist{lift_apos}), {lift_pos}")


def calibrieren_gabel_objects():
    print("GABEL OBJEKTE CALIBRIEREN!")
    robo.gabel.plimit(1)
    robo.gabel.run_to_position(OPEN_POS, 100)
    
    print("Turm halte postion!")
    ready_wait_for_start()
    robo.gabel.run_to_position(TURM_HALTE_POS, 15)
    gabel_apos= robo.gabel.get_aposition()
    gabel_pos= robo.gabel.get_position()
    print(f"Gabel:(soll{TURM_HALTE_POS} ist{gabel_apos}), {gabel_pos}")
    
    print("Artefakt halte postion!")
    ready_wait_for_start()
    robo.gabel.run_to_position(ARTEFAKT_HALTE_POS, 15)
    gabel_apos= robo.gabel.get_aposition()
    gabel_pos= robo.gabel.get_position()
    print(f"Gabel:(soll{ARTEFAKT_HALTE_POS} ist{gabel_apos}), {gabel_pos}")
    
    print("Besucher halte postion!")
    ready_wait_for_start()
    robo.gabel.run_to_position(BESUCHER_HALTE_POS, 15)
    gabel_apos= robo.gabel.get_aposition()
    gabel_pos= robo.gabel.get_position()
    print(f"Gabel:(soll{BESUCHER_HALTE_POS} ist{gabel_apos}), {gabel_pos}")
    ready_wait_for_start()
    
    
def print_pos():
    while True:
        while (not robo.button_rot.is_pressed) and (not robo.button_blau.is_pressed):
            time.sleep(0.1)              
        if robo.button_rot.is_pressed:
            break
        if robo.button_blau.is_pressed:
            lift_apos= robo.lift.get_aposition()
            lift_pos= robo.lift.get_position()
            gabel_apos= robo.gabel.get_aposition()
            gabel_pos= robo.gabel.get_position()
            print(f"Lift: {lift_apos}, {lift_pos} Gabel:{gabel_apos}, {gabel_pos}")
        while robo.button_blau.is_pressed:
             time.sleep(0.1) #wait for Button is released.              
      
            
        

def aufluepfen():
    robo.lift.run_for_rotations(2, 30)                                       
    robo.gabel.run_for_degrees(180, 50)
    robo.lift.run_for_rotations(-2, 30)





def run():
    lift_apos= robo.lift.get_aposition()
    lift_pos= robo.lift.get_position()
    gabel_apos= robo.gabel.get_aposition()
    gabel_pos= robo.gabel.get_position()
    print(f"Lift: {lift_apos}, {lift_pos} Gabel:{gabel_apos}, {gabel_apos}")

    #robo.gabel.off() # sensor off
    calibrieren_lift()
    calibrieren_gabel()
    calibrieren_gabel_objects()      
    print_pos()
   
    #robo.gabel.set_postion(0)
    #robo.gabel.set_apostion(0)
    gabel_apos= robo.gabel.get_aposition()
    gabel_pos= robo.gabel.get_position()
    print(f"Lift: {lift_apos}, {lift_pos} Gabel:{gabel_apos}, {gabel_apos}")
    
    
    
    
    #robo.lift.run_to_position(degrees, speed=None, blocking=True, direction='shortest')
    

    time.sleep(1)

    



def test():
    setup()
#    robo.fahren.plimit()
    ready_wait_for_start()
    run()      

    print("Wait on Button rot!")
    while not robo.button_rot.is_pressed:
        time.sleep(0.1)
    print("THE END!")

if __name__ == '__main__':
  test()
  #assert(False, "do not run directly"
  