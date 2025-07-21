from .core import LEDLang
import serial
import pty
import os
import threading
import argparse

# ANSI color codes for terminal output
WHITE = "\033[47m  \033[0m"
RED = "\033[41m  \033[0m"

class LEDDeviceSimulator:
    def __init__(self, master_fd):
        self.master_fd = master_fd
        self.grid_size = 5
        self.grid = [['WHITE' for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def print_grid(self):
        os.system('clear')  # clear terminal screen on update (Linux/macOS)
        print("5x5 LED Grid (WHITE = empty, RED = lit):")
        for row in self.grid:
            line = ''
            for color in row:
                if color == 'WHITE':
                    line += WHITE
                elif color == 'RED':
                    line += RED
            print(line)
        print("\nWaiting for commands...")

    def set_pixel(self, x, y, color):
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            self.grid[y][x] = color

    def clear_grid(self):
        self.grid = [['WHITE' for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def run(self):
        with os.fdopen(self.master_fd, 'rb+', buffering=0) as master:
            self.clear_grid()
            self.print_grid()
            buffer = b''
            while True:
                byte = master.read(1)
                if not byte:
                    continue
                if byte == b'\n':
                    line = buffer.decode('utf-8').strip()
                    buffer = b''
                    self.handle_command(line)
                else:
                    buffer += byte

    def handle_command(self, command):
        parts = command.split()
        if not parts:
            return
        cmd = parts[0].upper()
        if cmd == 'PLOT' and len(parts) == 3:
            try:
                x = int(parts[1])
                y = int(parts[2])
                self.set_pixel(x, y, 'RED')
                self.print_grid()
            except ValueError:
                pass
        elif cmd == 'CLEAR':
            self.clear_grid()
            self.print_grid()
        else:
            raise ValueError(f"Unknown command: {command}\nOn the real device, this would reset the device and return an error.")

def main():
    parser = argparse.ArgumentParser(description="LEDLang Tester.")
    parser.add_argument("folder", help="Folder that contains the LEDLang files.")
    parser.add_argument("animation", help="The file to play, without the .led extension.")
    args = parser.parse_args()

    # Setup virtual serial port pair
    master_fd, slave_fd = pty.openpty()
    slave_name = os.ttyname(slave_fd)

    # Start the device simulator in a thread
    simulator = LEDDeviceSimulator(master_fd)
    threading.Thread(target=simulator.run, daemon=True).start()

    with serial.Serial(slave_name, 115200, timeout=1) as ser:
        print(f"Listening on {slave_name} at 115200 baud...")

        LED = LEDLang(ser)
        LED.set_folder(args.folder)
        LED.playfile(args.animation + '.led')