import flet as ft
import os
import sys
from scanner import Scanner
from reporter import Reporter

def main(page: ft.Page):
    page.title = "NetPulse Python"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window_width = 1000
    page.window_height = 800

    scanner = Scanner()
    reporter = Reporter()

    # --- UI Components ---
    
    # Input for IP/Range
    ip_input = ft.TextField(
        label="Target IP / Range",
        hint_text="e.g., 192.168.1.1 or 192.168.1.0/24",
        width=400
    )

    # Scan Type Selector
    scan_type = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("Quick Scan"),
            ft.dropdown.Option("Full Scan"),
            ft.dropdown.Option("OS Detection"),
        ],
        value="Quick Scan"
    )

    # Progress Indicator
    progress_ring = ft.ProgressRing(visible=False)
    status_text = ft.Text("Ready", size=16)

    # Results Table
    results_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Host")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Open Ports")),
        ],
        rows=[]
    )

    # Export Button (Disabled initially)
    export_btn = ft.ElevatedButton("Export Report", disabled=True)

    # State for export
    current_scan_result = None

    def export_report(e):
        if current_scan_result:
            try:
                # Basic PDF generation
                filename = "scan_report.pdf"
                reporter.generate_pdf(current_scan_result, filename)
                
                dlg = ft.AlertDialog(
                    title=ft.Text("Success"),
                    content=ft.Text(f"Report saved to {filename}"),
                )
                page.dialog = dlg
                dlg.open = True
                page.update()
            except Exception as ex:
                print(f"Export error: {ex}")

    def on_scan_complete(nm, xml_output, error):
        nonlocal current_scan_result
        progress_ring.visible = False
        scan_btn.disabled = False
        
        if error:
            status_text.value = f"Error: {error}"
            status_text.color = "red"
        else:
            current_scan_result = nm
            status_text.value = "Scan Complete"
            status_text.color = "green"
            export_btn.disabled = False
            
            # Update Table
            results_table.rows.clear()
            for host in nm.all_hosts():
                status = nm[host]['status']['state']
                ports = []
                # Check if 'tcp' exists (common for -F)
                if 'tcp' in nm[host]:
                    lport = nm[host]['tcp'].keys()
                    for port in lport:
                        ports.append(str(port))
                
                results_table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(host)),
                        ft.DataCell(ft.Text(status)),
                        ft.DataCell(ft.Text(", ".join(ports))),
                    ])
                )
        
        page.update()

    def start_scan(e):
        target = ip_input.value
        if not target:
            ip_input.error_text = "Please enter a target"
            page.update()
            return
        
        ip_input.error_text = None
        progress_ring.visible = True
        status_text.value = "Scanning..."
        status_text.color = "cyan"
        scan_btn.disabled = True
        export_btn.disabled = True
        current_scan_result = None
        page.update()

        # Determine arguments based on selection
        args = "-F" # Default Quick
        if scan_type.value == "Full Scan":
            args = "-p-"
        elif scan_type.value == "OS Detection":
            args = "-O"

        scanner.scan_network(target, args, on_scan_complete)

    scan_btn = ft.ElevatedButton("Start Scan", on_click=start_scan)
    export_btn.on_click = export_report

    # --- Layout ---
    
    # Header
    header = ft.Row(
        [
            ft.Icon(ft.icons.WIFI, size=40, color=ft.colors.BLUE),
            ft.Text("NetPulse Scanner", size=30, weight=ft.FontWeight.BOLD)
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Controls Row
    controls = ft.Row(
        [ip_input, scan_type, scan_btn, progress_ring],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    # Main Column
    page.add(
        header,
        ft.Divider(height=20, thickness=1),
        controls,
        ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20, thickness=1),
        ft.Container(results_table, expand=True, padding=10),
        ft.Row([export_btn], alignment=ft.MainAxisAlignment.END)
    )

    # --- Startup Check ---
    if not scanner.check_nmap_installed():
        def close_dialog(e):
            page.window_close()
            
        dlg = ft.AlertDialog(
            title=ft.Text("Nmap Missing"),
            content=ft.Column([
                ft.Text("Nmap is not installed or not found in PATH."),
                ft.Text("Please install Nmap and Npcap to use this application."),
                ft.TextButton("Download Nmap", url="https://nmap.org/download.html")
            ], height=100),
            actions=[
                ft.TextButton("Close", on_click=close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

ft.app(target=main)
