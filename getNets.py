import platform
import subprocess

def writeFile(netList:dict, fileName:str) -> None:
    with open(fileName, "w", encoding="utf-8") as f:
        for k in netList:
            f.write(f"{k}: {netList[k]}\n")

def readFile(fileName:str) -> dict:
    ldict = {}
    with open(fileName, 'r', encoding="utf-8") as f:
        for line in f:
            key, value = line.strip().split(":", 1)
            ldict[key] = value
    return ldict

def getNetworkIP(ip:str, flag:bool) -> dict:
    v = ""
    # Linux
    if flag:
        try:
            cmd = f"host {ip}"
            output = subprocess.run([cmd], shell=True, timeout=3, check=True, capture_output=True, encoding="utf-8")
            output = output.stdout.split('\n')
            if output[0].__contains__("not found"):
                v = ""
            else:
                v = output[0].split()[-1]
        except (subprocess.CalledProcessError, TimeoutError, subprocess.TimeoutExpired):
            # print(f"{e.returncode}, {e.output}, {e.stderr}, {e.stdout}, {str(e)}")
            v = ""
    # Windows
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

    return {ip:v}


def main():
    # If os == Windows, set flag to False
    # If os == Linux, set flag to True
    flag = False
    name = platform.system()
    if name.startswith("Linux"):
        flag = True

    # We set up a dict that has key/value s.t. ip == key, returned == value
    retVals = {}
    # set up multithreading, and go through the IP range
    ip = "192.168.1."
    for i in range(0, 255):
        k = ip + str(i)
        v = getNetworkIP(k, flag)
        retVals[k] = v[k]

    # filter the empty space
    retVals = {k: v for k, v in retVals.items() if v != ""}
    print(retVals)
    writeFile(retVals, "./sample.txt")
    # backupIPs = doGetBackupIPs()
    # ciscoIPs = [key for key, value in retVals.items() if str(value).__contains__("Cisco")]
    # for ip in ciscoIPs:
    #     if len(backupIPs) == 0:
    #         doCiscoBackup(ip)
    #         # finish this
    # buffaloIPs = [key for key, value in retVals.items() if str(value).__contains__("Buffalo")]
    # for ip in buffaloIPs:
    #     print(f"{ip} needs to be upgraded")
    # # double check this
    # aristaIPs = [key for key, value in retVals.items() if str(value).__contains__("Arista")]
    # for ip in aristaIPs:
    #     doAristaBackup(ip)

if __name__ == "__main__":
    main()
