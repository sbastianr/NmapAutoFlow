import nmap
import shutil
import threading

class Scanner:
    def __init__(self):
        self.nm = None
    
    def check_nmap_installed(self):
        """Checks if Nmap is installed and available in the system path."""
        return shutil.which("nmap") is not None

    def scan_network(self, target, arguments, callback):
        """Runs the Nmap scan in a separate thread."""
        def run_scan():
            try:
                if self.nm is None:
                    self.nm = nmap.PortScanner()
                
                self.nm.scan(hosts=target, arguments=arguments)
                # Use XML output for reliable parsing as per rules
                xml_output = self.nm.get_nmap_last_output()
                callback(self.nm, xml_output, None)
            except Exception as e:
                callback(None, None, str(e))

        thread = threading.Thread(target=run_scan)
        thread.start()
