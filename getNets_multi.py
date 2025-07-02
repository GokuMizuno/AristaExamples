import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


def writeFile(netList: dict, fileName: str) -> None:
    with open(fileName, "w", encoding="utf-8") as f:
        for k in netList:
            f.write(f"{k}: {netList[k]}\n")


def readFile(fileName: str) -> dict:
    ldict = {}
    with open(fileName, 'r', encoding="utf-8") as f:
        for line in f:
            key, value = line.strip().split(":", 1)
            ldict[key] = value
    return ldict


def getNetworkIP(ip: str, flag: bool) -> tuple:
    v = ""
    if flag:
        try:
            cmd = f"host {ip}"
            output = subprocess.run(
                [cmd],
                shell=True,
                timeout=3,
                check=True,
                capture_output=True,
                encoding="utf-8"
            )
            output_lines = output.stdout.split('\n')
            if "not found" in output_lines[0]:
                v = ""
            else:
                v = output_lines[0].split()[-1]
        except (subprocess.CalledProcessError, TimeoutError, subprocess.TimeoutExpired):
            v = ""
    else:
        # Windows: use 'nslookup'
        try:
            cmd = f"nslookup {ip}"
            output = subprocess.run(
                [cmd],
                shell=True,
                timeout=3,
                check=True,
                capture_output=True,
                encoding="utf-8"
            )
            output_lines = output.stdout.split('\n')
            for line in output_lines:
                if line.strip().lower().startswith("name:"):
                    v = line.split(":", 1)[1].strip()
                    break
        except (subprocess.CalledProcessError, TimeoutError, subprocess.TimeoutExpired):
            v = ""

    return ip, v


def main():
    flag = platform.system().startswith("Linux")
    ip_prefix = "192.168.1."
    retVals = {}

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(getNetworkIP, ip_prefix + str(i), flag) for i in range(0, 255)]

        for future in as_completed(futures):
            ip, resolved = future.result()
            if resolved:
                retVals[ip] = resolved

    writeFile(retVals, "./sample_mult.txt")


if __name__ == "__main__":
    main()
