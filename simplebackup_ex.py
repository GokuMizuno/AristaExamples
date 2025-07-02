# sample project to backup a few different types of switches
# not for production use!

def getLoginInfo():
    # this is a dummy function that would normally read uname/pwd from either a file, or AD
    # here, we just pass a pretend uname/pwd
    return "ExampleName", "ExamplePwd"


def doAristaBackup(ip1: str, ip2: str = ""):
    # I don't have an arista device, so I cannot test this
    import pyeapi

    # --- Configuration ---
    SOURCE_SWITCH_IP = ip1
    SOURCE_USERNAME = 'YOUR_SOURCE_USERNAME'
    SOURCE_PASSWORD = 'YOUR_SOURCE_PASSWORD'

    DESTINATION_SWITCH_IP = ip2
    DESTINATION_USERNAME = 'YOUR_DESTINATION_USERNAME'
    DESTINATION_PASSWORD = 'YOUR_DESTINATION_PASSWORD'

    # --- Connect to Source Switch ---
    try:
        source_node = pyeapi.connect(
            host=SOURCE_SWITCH_IP,
            username=SOURCE_USERNAME,
            password=SOURCE_PASSWORD,
            return_node=True
        )
        print(f"Successfully connected to source switch: {SOURCE_SWITCH_IP}")
    except pyeapi.eapilib.eapi.EapiError as e:
        print(f"Error connecting to source switch: {str(e)}")
        exit()

    # --- Get Running Configuration from Source Switch ---
    try:
        response = source_node.enable('show running-config')
        running_config = response[0]['output']
        print("Successfully retrieved running configuration from source switch.")
    except pyeapi.eapilib.eapi.EapiError as e:
        print(f"Error retrieving configuration from source switch: {str(e)}")
        exit()

    # --- Connect to Destination Switch ---
    try:
        destination_node = pyeapi.connect(
            host=DESTINATION_SWITCH_IP,
            username=DESTINATION_USERNAME,
            password=DESTINATION_PASSWORD,
            return_node=True
        )
        print(f"Successfully connected to destination switch: {DESTINATION_SWITCH_IP}")
    except pyeapi.eapilib.eapi.EapiError as e:
        print(f"Error connecting to destination switch: {str(e)}")
        exit()

    # --- Apply Configuration to Destination Switch ---
    try:
        # Split the configuration into lines and send as a list of commands
        config_commands = running_config.splitlines()
        destination_node.config(config_commands)
        print("Successfully applied configuration to destination switch.")
    except pyeapi.eapilib.eapi.EapiError as e:
        print(f"Error applying configuration to destination switch: {str(e)}")
        exit()

    print("Backup and transfer process completed.")


def doCiscoBackup(ip1: str, ip2: str = ""):
    from netmiko import ConnectHandler

    uname, pwd = getLoginInfo()
    device = {
        "device_type": "cisco_ios",
        "ip": ip1,
        "username": uname,
        "password": pwd,
        # "secret": "YOUR_ENABLE_SECRET", # Optional, if using enable mode
    }

    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("show running-config")
    net_connect.disconnect()

    # After retrieving 'output' from source switch
    # If ip2 exists, copy over, else, write to file
    if ip2 != "":
        try:
            # First we try directly connecting via tftp
            device_dest = {
                "device_type": "cisco_ios",
                "ip": ip2,
                "username": uname,
                "password": pwd,
                # "secret": "YOUR_ENABLE_SECRET",
            }
            net_connect_dest = ConnectHandler(**device_dest)
            copy_command = "copy running-config tftp://TFTP_SERVER_IP/config_backup.txt"  # Example for TFTP
            net_connect_dest.send_command_timing(copy_command)
            # Handle prompts for filename, address, etc.
            net_connect_dest.disconnect()
        except:
            # This does the transfer via command line, not via tftp
            net_connect_dest = ConnectHandler(**device_dest)
            net_connect_dest.send_command("configure terminal")
            config_lines = output.splitlines()
            for line in config_lines:
                if line.strip() and not line.startswith("!"):  # Exclude comments and empty lines
                    net_connect_dest.send_command(line)
            net_connect_dest.send_command("end")
            net_connect_dest.send_command("write memory")  # Save configuration
            net_connect_dest.disconnect()
    else:
        ipFilename = str(ip1) + "_config.cfg"
        with open(ipFilename, 'w', encoding="utf-8") as f:
            f.write(output)
    # log and return success?


def doGetBackupIPs() -> list:
    # here we would get the list of IPs we are backing up our current machines to
    # this could be done via mac address, IP address, or some other method I don't know about
    # since I am mocking this, I'll just return []
    return []


def main():
    oldIPsfile = ""  # put the file name here, or call from args.  TODO: finish this
    oldDeviceIPs = []
    backupIPs = doGetBackupIPs()
    # Presuming the line is of the form {IP}, {Device name}
    # Think what is returned via host, or nslookup
    with open(oldIPsfile, 'r', encoding="utf-8") as file:
        for line in file:
            oldDeviceIPs.append(line)

    # There are more elegant ways of doing this, but I had this set up for something else, so I am cludging it
    oldDeviceIPs = dict(oldDeviceIPs)
    ciscoIPs = [key for key, value in oldDeviceIPs.items() if str(value).__contains__("Cisco")]
    for ip1, ip2 in zip(ciscoIPs, backupIPs):
        doCiscoBackup(ip1, ip2)
    backupIPs = backupIPs[len(ciscoIPs):]
    buffaloIPs = [key for key, value in oldDeviceIPs.items() if str(value).__contains__("Buffalo")]
    for ip in buffaloIPs:
        print(f"{ip} needs to be upgraded")
    # double check this
    aristaIPs = [key for key, value in oldDeviceIPs.items() if str(value).__contains__("Arista")]
    for ip1, ip2 in zip(aristaIPs, backupIPs):
        doAristaBackup(ip)
    backupIPs = backupIPs[len(aristaIPs):]


if __name__ == "__main__":
    main()
