# MdnsBroadcaster
Mdns Broadcaster is a tiny python program that forwards mDNS traffic from one or more network interface to each other.

This program was written to bring the ability of discovering devices from multiple network for Home Assistant. Home Assistant is capable to integrate devices only from a single network even if you expose multiple network to it. This is disadvantage for DIY home automation enthusiasists like me who would like to keep separate networks for IOTs often disconnected from Internet.

My expertise lie in Microsoft technologies and Python is greek to me. I have written this with the assistance of Microsoft Copilot. If you are an expert in Python and happen to find any bug or insane piece of code, feel free to raise a PR.

## Running the program
This program is required to be run only for discovering the devices and could be shutdown once the device is discovered and integrated. Apple HomeKit uses mDNS only for device discovery and then uses regular TCP/IP for continuous operation.

### Setup
1. Identify all the IP addresses of the network interfaces that you are using including physical and virtual.
1. Enter one IP address per line.
1. Save and close the file.
1. Allow UDP port 5353 on all the networks in your firewall. This can be disabled after the devices are discovered.
1. Execute the executable in the host machine / the machine that has all the network adapters.
1. If you are running this for HomeAssistant setup ensure Applekit Device is installed in your Home Assistant.

### Understanding the console messages.
The program execution has two steps.

1. Identifying the services that are broadcasting.

    Below is what it would look like.

    ```
    Starting mDNS Detector...
    Service added: _workstation._tcp.local.
    Service added: _home-assistant._tcp.local.
    Service added: _leap._tcp.local.
    Service added: _lap._tcp.local.
    Service added: _hap._tcp.local.
    Service added: _lutron._tcp.local.
    Service added: _hue._tcp.local.
    Service added: _http._tcp.local.
    Service added: _smb._tcp.local.
    Service added: _device-info._tcp.local.
    ```
    Depending on the mDNS services that is running in all of your network, the service list will change. If you are using this to setup HomeAssistant as I am, you should see _home-assistant._tcp.local and _hap._tcp.local.

1. Setting up mDNS traffic forwarding.

    A successful traffic forwarding will produce messages as below. Every one of the ip specified should show up in the log.

    ```
    Socket bound successfully to 20.0.0.2 on port 5353.
    Socket bound successfully to 10.0.0.100 on port 5353.
    Socket bound successfully to 172.17.0.1 on port 5353.
    ```
    
    If any of the IP is wrong or unresolvable, you may get an error like below.

    ```
    Failed to create mDNS socket on 2: [Errno 11001] getaddrinfo failed
    Failed to create mDNS socket on 0: [Errno 11001] getaddrinfo failed
    ```

Once the devices are discovered, the program can be shut down by Ctl + C. Ignore the thread abort error messages that gets logged into the console.