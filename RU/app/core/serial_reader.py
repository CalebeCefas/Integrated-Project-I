import serial

class SerialReader:
    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
    
    # Metodo para conectar com o Serial
    def __enter__(self):
        try:
            self.serial_connection = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

            if self.serial_connection.is_open:
                print(f"Conexão bem-sucedida à porta serial: {self.port}")
                return self
            else:
                print(f"Erro: Porta {self.port} não pôde ser aberta.")
                self.serial_connection = None
                return None
                
        except serial.SerialException as e:
            print(f"Erro ao conectar à porta serial {self.port}: {e}")
            self.serial_connection = None
            return None
        
        except Exception as e:
            print(f"Um erro inesperado ocorreu ao conectar: {e}")
            self.serial_connection = None
            return None

    # Metodo para fechar a conexão com o Serial
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
                print(f"Conexão com a porta {self.port} fechada.")
            elif self.serial_connection is None:
                print(f"Nenhuma conexão ativa para a porta {self.port} para fechar.")
            else:
                print(f"A porta {self.port} já está fechada.")
        except Exception as e:
            print(f"Erro ao fechar a conexão com a porta {self.port}: {e}")


    # Metodo para ler via Serial do arduino
    def read_data(self):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                data = self.serial_connection.readline().decode('utf-8').strip()
                return data
            except serial.SerialException as e:
                print(f"Erro de comunicação serial ao ler dados: {e}")
                return None
            except UnicodeDecodeError as e:
                print(f"Erro de decodificação ao ler dados: {e}. Dados brutos: {self.serial_connection.readline()}")
                return None
            except Exception as e:
                print(f"Erro inesperado ao ler dados: {e}")
                return None
        print("Erro: Conexão serial não está aberta para leitura.")
        return None