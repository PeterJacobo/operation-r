from flask import Flask, request, jsonify
from escpos.printer import Usb
import os
import traceback

app = Flask(__name__)

# USB Vendor and Product ID (replace with actual values from lsusb)
USB_VENDOR_ID = int(os.getenv("USB_VENDOR_ID", "0x1fc9"), 16)
USB_PRODUCT_ID = int(os.getenv("USB_PRODUCT_ID", "0x2016"), 16)

# Initialize printer
try:
    printer = Usb(USB_VENDOR_ID, USB_PRODUCT_ID)
except Exception as e:
    printer = None
    print(f"Printer connection failed: {e}")

@app.route("/print", methods=["POST"])
def print_task():
    if not printer:
        return jsonify({"error": "Printer not connected"}), 500

    data = request.get_json()
    task = data.get("task", "Test task from Operation R")
    source = data.get("source", "manual")

    try:
        printer.set(align='center', bold=True)
        printer.text(f"Task from {source}:\n")
        printer.text(f"{task}\n")
        printer.text("\n---\n")
        printer.cut()
        return jsonify({"status": "Printed successfully"}), 200
    except Exception as e:
        print("Error during printing:")
        traceback.print_exc()  # Logs full traceback to console
        return jsonify({"error": str(e)})

@app.route("/jira-webhook", methods=["POST"])
def jira_webhook():
    data = request.get_json()
    issue = data.get("issue", {})
    fields = issue.get("fields", {})
    summary = fields.get("summary", "No summary")
    key = issue.get("key", "No key")
    status = fields.get("status", {}).get("name", "Unknown")

    printer.set(align='center', bold=True)
    printer.text(f"Jira Task: {key}\n")
    printer.text(f"{summary}\n")
    printer.text(f"Status: {status}\n")
    printer.text("\n\n")
    printer.cut()

    return jsonify({"status": "Printed from Jira"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)