from fpdf import FPDF

class Reporter:
    def generate_pdf(self, scan_data, filename="report.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="NetPulse Scan Report", ln=1, align="C")
        
        pdf.ln(10)
        
        for host in scan_data.all_hosts():
            pdf.set_font("Arial", 'B', 12)
            hostname = scan_data[host].hostname()
            pdf.cell(0, 10, txt=f"Host: {host} ({hostname})", ln=1)
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 10, txt=f"State: {scan_data[host]['status']['state']}", ln=1)
            
            for proto in scan_data[host].all_protocols():
                pdf.cell(0, 10, txt=f"Protocol: {proto.upper()}", ln=1)
                lport = sorted(scan_data[host][proto].keys())
                for port in lport:
                    state = scan_data[host][proto][port]['state']
                    service = scan_data[host][proto][port]['name']
                    pdf.cell(0, 10, txt=f"  Port: {port} - {state} - {service}", ln=1)
            
            pdf.ln(5)
            
        pdf.output(filename)
        return filename

    def generate_html(self, scan_data, filename="report.html"):
        # Placeholder for HTML report generation
        pass
