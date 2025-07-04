import platform
import subprocess


def writeFile(netList: dict, fileName: str) -> None:
    '''
    Writes data to a text file

    Args:
        netList (dict):  A dictionary of IP: name of object
        fileName (str):  the full path to the file

    Returns:
        Nothing

    Raises:
        Nothing
    '''
    with open(fileName, "w", encoding="utf-8") as f:
        for k in netList:
            f.write(f"{k}: {netList[k]}\n")


def readFile(fileName: str) -> dict:
    """
    Reads data into a dictionary from a file

    Args:
        fileName (str):  the path to the file

    Returns:
        A dictionary {IP: name}

    Raises:
        Nothing
    """
    ldict = {}
    with open(fileName, 'r', encoding="utf-8") as f:
        for line in f:
            key, value = line.strip().split(":", 1)
            ldict[key] = value
    return ldict


def getNetworkIP(ip: str, flag: bool) -> tuple:
    """
    Tests all network IPs on my local 192.168.1 subnet

    Args:
        ip (str):  the IP address to test
        flag (bool): use the Linux or Windows commands

    Returns:
        tuple (str, str): (ip address), name, or blank string

    Raises:
        Exception if any errors are raised
    """
    v = ""
    # Linux, uses host
    if flag:
        try:
            cmd = f"host {ip}"
            output = subprocess.run([cmd], shell=True, timeout=3, check=True, capture_output=True, encoding="utf-8")
            output = output.stdout.split('\n')
            if "not found" in output[0]:
                v = ""
            else:
                v = output[0].split()[-1]
        except (subprocess.CalledProcessError, TimeoutError, subprocess.TimeoutExpired):
            v = ""
    # Windows, uses nslookup
    else:
        try:
            cmd = f"nslookup {ip}"
            output = subprocess.run([cmd], shell=True, timeout=3, check=True, capture_output=True, encoding="utf-8")
            output_lines = output.stdout.split('\n')
            for line in output_lines:
                if line.strip().lower().startswith("name:"):
                    v = line.split(":", 1)[1].strip()
                    break
        except (subprocess.CalledProcessError, TimeoutError, subprocess.TimeoutExpired):
            v = ""

    return ip, v


def main():
    # If os == Windows, set flag to False
    # If os == Linux, set flag to True
    flag = False
    name = platform.system()
    if name.startswith("Linux"):
        flag = True

    retVals = {}
    ip = "192.168.1."
    for i in range(0, 255):
        k = ip + str(i)
        fullip, v = getNetworkIP(k, flag)
        # filter the empty space
        if v:
            retVals[fullip] = v
    writeFile(retVals, "./sample.txt")


if __name__ == "__main__":
    main()
