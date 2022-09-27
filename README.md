# FarmBOX-Firmware-Latest
Firmware for FarmBOX's Raspberry Pi


Issues we faced an how other community members can overcome them:


Python Dependencies conflict each other. Look into a Python Virtual Enviornment https://docs.python.org/3/library/venv.html


Create one venv for the package causing the conflicting dependency (in our case TensorFlow), and leave the normal python environment for everything else.


Pip SSL Error. This means that your computer is behind a Proxy. Install a VPN like ProtonVPN (it's free), and the issues will go away. https://protonvpn.com/
