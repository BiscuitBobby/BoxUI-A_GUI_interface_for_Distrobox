import subprocess
from Data.FetchData import DistroList


def get_default_terminal():
    try:
        command = ['gnome-terminal', '-e', 'ls']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            raise RuntimeError(f"Command {command} failed with error message: {stderr.decode().strip()}")
        process.terminate()
        return 'gnome-terminal'

    except:
        try:
            command = ['konsole', '-e', 'ls']
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                raise RuntimeError(f"Command {command} failed with error message: {stderr.decode().strip()}")
            process.terminate()
            return 'konsole'
        except:
            try:
                command = ['xdg-terminal', '-e', 'ls']
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if stderr:
                    raise RuntimeError(f"Command {command} failed with error message: {stderr.decode().strip()}")
                process.terminate()
                return 'xdg-terminal'
            except:
                print("cannot find terminal\ndownload gnome shell?")

terminal = get_default_terminal()
print('\n',terminal)

def enter_distro(name):
    subprocess.run([terminal, '-e', 'distrobox', 'enter', name.strip()])

def remove_distro(name):
    subprocess.run(['distrobox', 'rm', name.strip()], input='y\n', text=True)
    DistroList()
def stop_distro(name):
    subprocess.run(['distrobox', 'stop', name.strip()], input='y\n', text=True)
    DistroList()
def start_distro(name):
    subprocess.run(['distrobox', 'enter', name.strip()])
    DistroList()
