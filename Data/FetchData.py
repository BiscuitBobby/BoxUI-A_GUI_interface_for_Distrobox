import sys
try:
    import importlib.util
except:
    print("cant import importlib.util")
    sys.exit()


# Check if required modules are available
for module_name in ['subprocess', 'os']:
    if importlib.util.find_spec(module_name) is None:
        print(f"Cannot access {module_name} module")
        sys.exit()
import os
import subprocess
dists = dict()


def update(name, status='Unknown', id='Unknown', distro="unknown"):
    if id not in dists:
        icon = icons(distro.split(':')[0].split('-')[0])
        dists[id] = {"name": name, "icon": icon, "status": status, "id": id, "distro": distro}
        dists[id][status] = status
        dists[id][name] = name
        dists[id][id] = id


def icons(name):
    home_dir = os.path.expanduser("~")
    try:
        icons_dir = os.path.join(home_dir, ".local", "share", "icons", "distrobox")
        for root, dirs, files in os.walk(icons_dir):
            for file in files:
                if file.startswith(name.lower()):
                    distros_dir = os.path.join(root, file)
                    # print(f"Found icon at {distros_dir}")
                    return distros_dir
    except:
        return ''


def DistroList():
    global dists
    dists = dict()
    process = subprocess.Popen(['distrobox', 'list'], stdout=subprocess.PIPE)
    output = process.stdout.readline().strip()

    while output:
        output = process.stdout.readline().strip().decode("utf-8")
        x = output.split('|')  # splits ID, NAME, STATUS and IMAGE

        distro = (x[-1].split('/')[-1])
        if distro != '':
            status = (x[2]).strip()
            id = (x[0]).strip()
            name = x[1]
            update(name, status, id, distro)  # decode("utf-8") converts bytes to string
    return dists
