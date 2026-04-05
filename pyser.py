import serial
import time
import pyautogui

# Change COM port (Windows: COM3, COM4... / Linux: /dev/ttyUSB0)
ser = serial.Serial('COM12', 9600, timeout=1)

time.sleep(2)  # wait for Arduino reset

while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
    
        
        try:
            number = int(data)
            
            if number == 1:
                print("Received 1")
                pyautogui.press('delete')  # Simulate pressing the 'Delete' key
            elif number == 2:
                print("Received 2")
                pyautogui.press('enter')
            elif number == 3:
                print("Received 3")
                pyautogui.press('down')
                
        except ValueError:
            pass