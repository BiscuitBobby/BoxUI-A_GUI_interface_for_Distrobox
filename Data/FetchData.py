import os
import subprocess
dists = dict()


def update(name, status='Unknown'):
    if name not in dists:
        icon = icons(name.split(':')[0])
        dists[name] = {"icon": icon, "status": status}
    else:
        dists[name][status] = status


def icons(name):
    home_dir = os.path.expanduser("~")
    try:
        icons_dir = os.path.join(home_dir, ".local", "share", "icons", "distrobox")
        for root, dirs, files in os.walk(icons_dir):
            for file in files:
                if file.startswith(name):
                    distros_dir = os.path.join(root, file)
                    # print(f"Found icon at {distros_dir}")
                    return distros_dir
    except:
        return None

    return None


def DList():
    process = subprocess.Popen(['distrobox', 'list'], stdout=subprocess.PIPE)
    output = process.stdout.readline().strip()

    while output:
        print(output)
        output = process.stdout.readline().strip().decode("utf-8")

        name = (output.split('/')[-1])
        if name != '':
            status = ((output.split('|'))[2]).strip()
            update(name, status)  # decode("utf-8") converts bytes to string

DList()
print(dists)