import os
import time

def obtener_info_cpu():
    """Obtener uso de CPU desde /proc/stat"""
    with open('/proc/stat', 'r') as f:
        line = f.readline().split()
        cpu = line[0]
        user = int(line[1])
        nice = int(line[2])
        system = int(line[3])
        idle = int(line[4])
        iowait = int(line[5])
        irq = int(line[6])
        softirq = int(line[7])
        total = user + nice + system + idle + iowait + irq + softirq
        uso_cpu = (user + nice + system) / total * 100
        return uso_cpu

def obtener_info_memoria():
    """Obtener uso de memoria desde /proc/meminfo"""
    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()
        memoria_total = int(lines[0].split()[1])  # Memoria total (en kB)
        memoria_libre = int(lines[1].split()[1])  # Memoria libre (en kB)
        memoria_usable = int(lines[2].split()[1]) # Memoria usable (en kB)
        memoria_usada = memoria_total - memoria_libre
        return memoria_total, memoria_usada, memoria_libre

def obtener_info_procesos():
    """Obtener información de los primeros 5 procesos en /proc/[PID]/status"""
    procesos = []
    for pid in os.listdir('/proc'):
        if pid.isdigit():
            try:
                with open(f'/proc/{pid}/status', 'r') as f:
                    lines = f.readlines()
                    name = lines[0].split(':')[1].strip()
                    state = lines[2].split(':')[1].strip()
                    processes = {'PID': pid, 'Name': name, 'State': state}
                    procesos.append(processes)
            except:
                continue
    return procesos

def mostrar_info():
    """Mostrar el monitoreo en tiempo real de CPU, memoria y procesos"""
    while True:
        uso_cpu = obtener_info_cpu()
        memoria_total, memoria_usada, memoria_libre = obtener_info_memoria()
        procesos = obtener_info_procesos()

        # Imprimir la información en pantalla
        print(f"\n--- Monitor de Recursos ---")
        print(f"Uso de CPU: {uso_cpu:.2f}%")
        print(f"Memoria Total: {memoria_total / 1024:.2f} MB")
        print(f"Memoria Usada: {memoria_usada / 1024:.2f} MB")
        print(f"Memoria Libre: {memoria_libre / 1024:.2f} MB")
        print(f"\nPrimeros 5 Procesos:")
        for proceso in procesos[:5]:
            print(f"PID: {proceso['PID']} | Name: {proceso['Name']} | Estado: {proceso['State']}")
        
        # Pausar el ciclo por 5 segundos antes de mostrar nuevamente la información
        time.sleep(5)

if __name__ == "__main__":
    mostrar_info()
