import subprocess
import sys

try:
    import prompt_toolkit
except ImportError:
    subprocess.run([f"{sys.executable} -m pip install prompt-toolkit"])

from prompt_toolkit.shortcuts import (checkboxlist_dialog, input_dialog,
                                      message_dialog, radiolist_dialog)
from prompt_toolkit.shortcuts.dialogs import yes_no_dialog
from prompt_toolkit.styles import Style

style = Style.from_dict({
    "dialog": "bg:#88ff88",
    "dialog frame-label": "bg:#ffffff #000000",
    "dialog.body": "bg:#000000 #00ff00",
    "dialog shadow": "bg:#00aa00",
})

mirror = "http://129.159.252.36"


class Switch():
    QUIT = 0
    
    class Modes():
        INSTALL = 1
        REPAIR = 2
        UPGRADE = 3
        THEMES = 4
        ICONS = 5
        OCI = 6

    class Install():
        BUNDLES = 1
        PACKAGES = 2
        AUTOMATIZED = 3

    class OCI():
        OPEN_PORT = 1
        INSTALL_OPENVPN = 2

while True:
    main_result = radiolist_dialog(
        title="Linux CLI Toolkit",
        text="Select mode",
        values=[[Switch.Modes.INSTALL, "Install"], [Switch.Modes.REPAIR, "Repair"], [Switch.Modes.UPGRADE, "Upgrade"], [Switch.Modes.OCI, "OCI"], [Switch.QUIT, "QUIT"]],
        style=style
    ).run()

    if main_result == Switch.Modes.UPGRADE:
        subprocess.run(["sudo apt update && sudo apt upgrade -y"], shell=True)
    elif main_result == Switch.Modes.REPAIR:
        subprocess.run(["sudo apt install --fix-broken"], shell=True)
    elif main_result == Switch.Modes.INSTALL:
        install_result = radiolist_dialog(
            title="Linux CLI Toolkit",
            text="Select mode",
            values=[[Switch.Install.BUNDLES, "Bundles"],
                    [Switch.Install.PACKAGES, "Packages"]],
            style=style
        ).run()

        if install_result == Switch.Install.BUNDLES:
            bundles = {
                "Networking": ["net-tools", "wireless-tools"],
                "Wireless hacking": ["aircrack-ng", "wifite", "hashcat"]
            }

            bundles_result = checkboxlist_dialog(
                title="Linux CLI Toolkit",
                text="Select bundles",
                values=[[bundles[i], i] for i in bundles],
                style=style
            ).run()

            subprocess.run(["sudo apt update"], shell=True)
            subprocess.run(
                [f"sudo apt install {' '.join([' '.join(i) for i in bundles_result])}"], shell=True)

        elif install_result == Switch.Install.PACKAGES:
            packages = {k: v for k, v in sorted({
                "nmap": "Nmap",
                "hashcat": "Hashcat",
                "hashcat-nvidia": "Hashcat - NVIDIA",
                "net-tools": "Ubuntu net tools",
                "wifite": "Wifite",
                "git": "Git",
                "ufw": "Ubuntu firewall",
                "apache2": "Apache2 webserver",
                "python3": "Python3",
                "python3-pip": "PIP for Python3",
                "python2": "Python3",
                "nano": "Nano editor",
                "vim": "Vim editor",
                "code": "Visual Studio Code",
                "gparted": "GParted",
                "htop": "Htop",
                "neofetch": "Neofetch",
                "virtualbox": "Virtualbox",
                "hydra": "Hydra",
                "hping3": "Hping3",
                "firewalld": "Firewall-cmd"
            }.items(), key=lambda item: item[1], reverse=False)}

            packages_result = checkboxlist_dialog(
                title="Linux CLI Toolkit",
                text="Select packages",
                values=[[i, packages[i]] for i in packages],
                style=style
            ).run()

            if packages_result != []:
                subprocess.run(["sudo apt update"], shell=True)
                subprocess.run(
                    [f"sudo apt install {' '.join(packages_result)}"], shell=True)
    elif main_result == Switch.Modes.OCI:
        oci_result = radiolist_dialog(
            title="Linux CLI Toolkit",
            text="Select mode",
            values=[[Switch.OCI.INSTALL_OPENVPN, "Install OpenVPN"],
                    [Switch.OCI.OPEN_PORT, "Open port"]],
            style=style
        ).run()

        if oci_result == Switch.OCI.OPEN_PORT:
            tcp = yes_no_dialog(
                title="Linux CLI Toolkit",
                text="Select protocol",
                yes_text="TCP",
                no_text="UDP",
                style=style
            ).run()

            port = input_dialog(
                title="Linux CLI Toolkit",
                text="Port(s) to open",
                style=style
            ).run()

            subprocess.run(
                [f"sudo firewall-cmd --zone=public --permanent --add-port={port}/{'tcp' if tcp else 'udp'}"], shell=True)
            subprocess.run(["sudo firewall-cmd --reload"], shell=True)

        elif oci_result == Switch.OCI.INSTALL_OPENVPN:
            subprocess.run(["sudo apt update"], shell=True)
            subprocess.run(["sudo apt install firewalld"], shell=True)

            subprocess.run(
                ["curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh"], shell=True)
            subprocess.run(["chmod +x openvpn-install.sh"], shell=True)
            subprocess.run(["sudo bash openvpn-install.sh"], shell=True)

            tcp = yes_no_dialog(
                title="Linux CLI Toolkit",
                text="Select PROTOCOL you have chosen",
                yes_text="TCP",
                no_text="UDP",
                style=style
            ).run()
            port = input_dialog(
                title="Linux CLI Toolkit",
                text="Select PORT you have chosen",
                style=style
            ).run()
            subprocess.run(
                [f"sudo firewall-cmd --zone=public --permanent --add-port={port}/{'tcp' if tcp else 'udp'}"], shell=True)
            subprocess.run(["sudo firewall-cmd --reload"], shell=True)

            subprocess.run(["sudo systemctl status openvpn"], shell=True)
    elif main_result == Switch.QUIT:
        exit(0)
