# MdnsBroadcaster

**MdnsBroadcaster** is a lightweight Python program that forwards mDNS traffic between multiple network interfaces.

This tool was developed to enable device discovery across multiple networks for **Home Assistant**. By default, Home Assistant integrates devices only from a single network, even when multiple networks are exposed to it. This limitation can be frustrating for DIY home automation enthusiasts like myself, who often maintain separate networks for IoT devices—frequently isolated from the internet.

My expertise lies in Microsoft technologies, and Python is greek to me (literally). This program was written with the help of **Microsoft Copilot**. If you're a Python expert and spot any bugs or insane code, feel free to contribute by raising a Pull Request (PR).

---

## Running the Program

This program only needs to be run during the device discovery phase. Once a device has been discovered and integrated, the program can be shut down. Apple HomeKit uses mDNS exclusively for device discovery, while regular TCP/IP is used for ongoing operations.

### Pre-Requisites

1. Allow **UDP port 5353** on all your networks through the firewall. This can be disabled once the devices are discovered.
2. For **Home Assistant**, ensure the **AppleKit Device** integration is installed.
3. Install **Python**.
4. Download the repository and extract its contents to a folder.
5. Navigate to the folder in your terminal.
6. Run the command:  
   ```
   pip install -r requirements.txt
   ```

### Setup

1. Identify all the IP addresses of your network interfaces (both physical and virtual).
2. Enter one IP address per line in the `iplist.txt` file.
3. Save and close the file.
4. Run the program in the terminal:  
   ```
   python Main.py
   ```

---

## Understanding the Console Messages

The program's execution is divided into two steps:

### 1. Identifying Broadcasting Services

The program starts by detecting broadcasting services. Here's an example of what you might see:

```
Starting mDNS Detector...
Service added: _workstation._tcp.local.
Service added: _home-assistant._tcp.local.
Service added: _leap._tcp.local.
Service added: _hap._tcp.local.
Service added: _lutron._tcp.local.
Service added: _hue._tcp.local.
Service added: _http._tcp.local.
Service added: _smb._tcp.local.
Service added: _device-info._tcp.local.
```

The list of detected services will depend on the mDNS services running on your networks. For a **Home Assistant** setup, you should see services like `_home-assistant._tcp.local` and `_hap._tcp.local`.

### 2. Setting Up mDNS Traffic Forwarding

Once traffic forwarding is successfully set up, you should see messages like the following for each specified IP:

```
Socket bound successfully to 20.0.0.2 on port 5353.
Socket bound successfully to 10.0.0.100 on port 5353.
Socket bound successfully to 172.17.0.1 on port 5353.
```

If any IP addresses are incorrect or unresolved, you might encounter errors like this:

```
Failed to create mDNS socket on 2: [Errno 11001] getaddrinfo failed
Failed to create mDNS socket on 0: [Errno 11001] getaddrinfo failed
```

---

## Shutting Down

Once all devices are discovered, you can safely terminate the program by pressing `Ctrl + C`. You may see thread abort errors in the console—these can be ignored.

---
