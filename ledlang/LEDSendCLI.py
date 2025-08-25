from .core import LEDLang
import serial
from pathlib import Path
import os
import argparse
from pathlib import Path
from rich.console import Console
from rich.text import Text
import logging
import subprocess

console = Console()

ourdir = os.path.abspath(os.path.dirname(__file__))
tests = os.path.abspath(ourdir + "/tests")

def main():
    parser = argparse.ArgumentParser(description="LEDLang CLI Sender.")
    parser.add_argument("--folder", help="Folder that contains the LEDLang files. Defaults to the libs tests folder.", default=tests)
    parser.add_argument("animation", help="The file to play, without the .led extension.")
    parser.add_argument("serial", type=Path, help="The serial port to connect to (e.g., /dev/ttyUSB0).")
    parser.add_argument("--baudrate", type=int, help="The baud rate to use (e.g., 115200).", default=115200)
    args = parser.parse_args()
    args.serial = str(args.serial)

    with serial.Serial(args.serial, args.baudrate, timeout=1) as ser:
        print(f"Listening on {args.serial} at {args.baudrate} baud...")

        LED = LEDLang(ser)
        LED.set_folder(args.folder)
        LED.playfile(args.animation)

        # Check serial output for errors
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue
            logging.info(line)
            if line.startswith("Error:"):
                raise RuntimeError(f"Received error from LEDLang: {line}")

def list_files():
    """
    List all animations in tests
    """
    tests_path = Path(tests)
    
    if not tests_path.exists() or not tests_path.is_dir():
        console.print(f"[red]Error:[/red] '{tests}' is not a valid directory.")
        return
    
    files = [f.stem for f in tests_path.iterdir() if f.is_file()]
    
    if not files:
        console.print(f"[yellow]No files found in '{tests}'[/yellow]")
        return
    
    console.print(f"[bold green]Files in {tests_path.name}:[/bold green]")
    for filename in files:
        console.print(Text(filename, style="cyan"))

def PyTestTestingCLI():
    parser = argparse.ArgumentParser(description="Run LEDLang tests with PyTest.")
    subprocess.run(["pytest"], cwd=ourdir + "/pytests")