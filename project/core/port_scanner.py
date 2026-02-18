import psutil
import ipaddress
import ctypes
import ctypes.wintypes as wintypes
import os


class PortScanner:

    def __init__(self, conn_type:str):
        self.connections = self.get_connections(conn_type)


    #--------------- get opened connections ---------------#
    def get_connections(self, conn_type:str):
        connections = []
        conn_type = conn_type.upper()

    
        #: check conn_type :#
        if conn_type not in ['ESTABLISHED', 'LISTEN']:
            return f'{conn_type} not valid!\nconnect type most be - ESTABLISHED OR LISTEN -'
            

        for conn in psutil.net_connections(kind="inet"):

            if conn.status != conn_type:
                continue
            
            #- in listen connection -#
            connection_data = {
                "pid": conn.pid,
                "local_ip": conn.laddr.ip if conn.laddr else None,
                "local_port": conn.laddr.port if conn.laddr else None,
            }

            #- just when connection established -#
            if conn_type == psutil.CONN_ESTABLISHED:
                remote_ip = conn.raddr.ip if conn.raddr else None
                remote_port = conn.raddr.port if conn.raddr else None

                connection_data["remote_ip"] = remote_ip
                connection_data["remote_port"] = remote_port
                connection_data["ip_type"] = self.classify_ip(remote_ip)
            
            #- get pid name and path -#
            if conn.pid:
                try:
                    proc = psutil.Process(conn.pid)
                    connection_data["process"] = {
                        "name": proc.name(),
                        "status": proc.status(),
                        "exe": proc.exe(),
                    }

                    #- check if runing in system32 -#
                    exe_path = proc.exe()
                    connection_data["is_system32"] = self.is_in_system32(exe_path)


                    #- check if runing as admin -#
                    connection_data['is_admin'] = self.is_runing_as_admin(conn.pid)

                except psutil.AccessDenied:
                    connection_data["process"] = "Access Denied"
                    connection_data["is_admin"] = False

            #- adding risk score
            connection_data["risk_score"] = self.calculate_risk(connection_data)

            connections.append(connection_data)

        #- sort list by highest risk -#
        connections = sorted(connections, key=lambda x: x.get("risk_score", 0), reverse=True)
        return connections
    
    
    #--------------- established connections IP scanner ---------------#
    def classify_ip(self, ip):
        if not ip:
            return "NO_REMOTE"

        ip_obj = ipaddress.ip_address(ip)

        if ip_obj.is_private:
            return "PRIVATE"

        if ip_obj.is_loopback:
            return "LOOPBACK"

        if ip_obj.is_reserved:
            return "RESERVED"

        return "PUBLIC"
    

    #--------------- established connections PORT scanner ---------------#
    def classify_port(self, port):
        if port in [80, 443, 22, 21, 25, 53]:
            return "COMMON"
        elif 0 <= port <= 1023:
            return "SYSTEM"
        elif 1024 <= port <= 49151:
            return "REGISTERED"
        elif port >= 49152:
            return "DYNAMIC"
        else:
            return "SUSPICIOUS"
    

    #--------------- risk scor ---------------#
    def calculate_risk(self, conn):
        score = 0

        #- Port
        port_type = self.classify_port(conn["local_port"])
        if port_type == "SYSTEM":
            score += 0
        elif port_type == "COMMON":
            score += 5
        elif port_type == "REGISTERED":
            score += 10
        elif port_type == "DYNAMIC":
            score += 5
        elif port_type == "SUSPICIOUS":
            score += 50

        #- Remote IP (فقط إذا موجود)
        ip_type = conn.get("ip_type")
        if ip_type == "PUBLIC":
            score += 20
        elif ip_type in ["PRIVATE", "LOOPBACK"]:
            score += 0

        #- Process path
        proc = conn.get("process")
        if isinstance(proc, dict):
            exe = proc.get("exe", "").lower()
            if any(folder in exe for folder in ["appdata", "temp", "downloads"]):
                score += 30

        #- Remote Port suspicious (فقط إذا موجود)
        remote_port = conn.get("remote_port")
        if remote_port in [4444, 1337, 6666, 9001, 12345]:
            score += 50

        #- LISTEN IP check
        local_ip = conn.get("local_ip")
        if local_ip == "0.0.0.0":
            score += 30

        if conn.get("is_admin"):
            score += 20
                                
        if not conn.get("is_system32") and conn.get("is_admin"):
            score += 30

        return min(score, 100)
    
    
    #--------------- check if program runing as admin ---------------#
    def is_runing_as_admin(self, pid):
        try:
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            TOKEN_QUERY = 0x0008
            TokenElevation = 20

            kernel32 = ctypes.windll.kernel32
            advapi32 = ctypes.windll.advapi32

            hProcess = kernel32.OpenProcess(
                PROCESS_QUERY_LIMITED_INFORMATION,
                False,
                pid
            )

            if not hProcess:
                return False

            hToken = wintypes.HANDLE()

            if not advapi32.OpenProcessToken(
                hProcess,
                TOKEN_QUERY,
                ctypes.byref(hToken)
            ):
                kernel32.CloseHandle(hProcess)
                return False

            elevation = wintypes.DWORD()
            size = wintypes.DWORD()

            result = advapi32.GetTokenInformation(
                hToken,
                TokenElevation,
                ctypes.byref(elevation),
                ctypes.sizeof(elevation),
                ctypes.byref(size),
            )

            #- close handles properly
            kernel32.CloseHandle(hToken)
            kernel32.CloseHandle(hProcess)

            if not result:
                return False

            return bool(elevation.value)

        except:
            return False
        
    
    #--------------- check if program runing in System32 ---------------#
    def is_in_system32(self, exe_path):
        if not exe_path:
            return False

        exe_path = exe_path.lower()

        system32_path = os.path.join(
            os.environ.get("WINDIR", "C:\\Windows"),
            "System32"
        ).lower()

        return True if exe_path.startswith(system32_path) else False




# x = PortScanner('listen')
# # SystemLogger('info', 'scanning result (Listen Connections)', x.connections)
# print(x.connections)


