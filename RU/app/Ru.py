import serial

porta_serial = 'COM3'
baud_rate = 9600
timeout = 1

try:
    ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)
    
    while True:
        linha = ser.readline().decode('utf-8', errors='ignore').strip()
        if linha:
            print("Arduino disse:", linha)

except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial: {e}")

