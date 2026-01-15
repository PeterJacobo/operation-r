# 🖨️ Operation R: Email & Jira Task Printing for Kanban

**Operation R** is a robust CLI tool that automates printing emails and Jira tickets to a thermal printer for physical Kanban task management. Turn digital tasks into tangible post-it note sized printouts!

---

## ✨ Features

- 📨 **Gmail Integration**: Automatically monitor and print emails labeled with `KanbanPrint`
- 🎫 **Jira Ticket Printing**: Print Jira tickets from XML exports with clean, readable formatting
- 🏷️ **Large Label Printing**: Create large ASCII art labels rotated 90° for Kanban lane headers
- 📊 **Barcode Generation**: Generate scannable barcodes (CODE128, CODE39, EAN13, UPC-A, and more)
- 🐾 **ASCII Animals**: AI-generated ASCII art using lightweight local LLM (no storage needed!)
- 🖨️ **Flexible Printer Support**: USB or network connection for thermal printers
- 🎛️ **Interactive Setup Wizard**: Easy printer configuration for USB or network printers
- 🎛️ **Interactive CLI Menu**: User-friendly numbered menu for all operations
- 📝 **Smart Label Management**: Tracks printed emails to avoid duplicates
- 🌐 **Web Server**: Flask API endpoints for webhooks and remote printing
- 🧪 **Test Printing**: Verify printer setup with ASCII art test page

---

## 🧰 Tech Stack

| Component      | Technology           |
|----------------|---------------------|
| Language       | Python 3.11         |
| Printer Driver | python-escpos       |
| Email API      | Gmail API           |
| Web Framework  | Flask               |
| Hardware       | Thermal Printers (USB/Network) |
| Platform       | Windows 11 / Linux / macOS |

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/PeterJacobo/operation-r.git
cd operation-r
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\Activate.ps1  # Windows PowerShell
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Printer
Run the interactive setup wizard to configure your printer connection:
```bash
python main.py setup
```

The wizard will guide you through:
- Choosing between USB or network connection
- Entering printer connection details (USB IDs or IP address)
- Testing the printer connection
- Saving configuration to `.env` file

Alternatively, manually edit `.env`:
```bash
cp .env.example .env
```
### 6. Install USB Driver (Windows - USB Printers Only)
If using USB connection on Windows:

Download libusb from: https://github.com/libusb/libusb/releases
Extract `libusb-1.0.dll` to `C:\Windows\System32`

**Note**: Network printers don't require USB drivers.
- `USB_VENDOR_ID`: Printer USB vendor ID (default: 0x0FE6)
- `USB_PRODUCT_ID`: Printer USB product ID (default: 0x811E)

For network printers:
- `PRINTER_CONNECTION_TYPE=network`
- `PRINTER_IP`: Printer IP address (e.g., 192.168.1.100)
This launches a numbered menu:
```
========================================
Operation R - Main Menu
========================================
1. Fetch emails (start monitoring service)
2. Reset labels (remove 'Printed' labels)
3. Setup printer (configure USB/network)
4. Test print (verify printer setup)
5. Print ticket (from XML)
6. Print label (large text, rotated 90°)
7. Start web server
0. Exit
========================================
```

### Command Line Usage

**Setup Printer**:
```bash
python main.py setup
```
Interactive wizard to configure USB or network printer connection.

**ASCII Animals (AI-Generated) 🐾**:
```bash
python main.py animals
# Or generate a specific animal:
python main.py animals dragon
python main.py animals cat
```
Generate unique ASCII art of animals using a lightweight local LLM! See [ASCII_ANIMALS.md](ASCII_ANIMALS.md) for details.

**Fetch and Print Emails**:
### Interactive Menu (Recommended)
```bash
python main.py
```

This launches a numbered menu:
```
========================================
Operation R - Main Menu
========================================
1. Fetch emails (start monitoring service)
2. Reset labels (remove 'Printed' labels)
3. Setup printer (configure USB/network)
4. Test print (verify printer setup)
5. Print ticket (from XML)
6. Print label (large text, rotated 90°)
7. Print barcode (scannable barcode)
8. ASCII Animals 🐾 (AI-generated art)
9. Start web server
0. Exit
========================================
```

### Command Line Usage

**Fetch and Print Emails**:
```bash
python main.py fetch
```
Monitors Gmail every 10 minutes for emails with `KanbanPrint` label.

**Print Jira Ticket**:
```bash
python main.py print-ticket
# Or specify file directly:
python main.py print-ticket tickets/QCWEB-4613.xml
```

**Print Large Label**:
```bash
python main.py print-label TODO
python main.py print-label IN PROGRESS
python main.py print-label DONE
```
Creates large ASCII art labels rotated 90° for visibility from a distance.

**Print Barcode**:
```bash
python main.py barcode "Hello123"
python main.py barcode "TICKET-2024-001" --type CODE39
python main.py barcode "1234567890128" --type EAN13 --height 150
python main.py barcode --list  # Show all supported barcode types
python main.py barcode --list-examples  # Show format examples
```
Generate scannable barcodes for tickets, inventory, URLs, and more. Supports CODE128, CODE39, EAN13, UPC-A, and more.

**Test Printer**:
```bash
python main.py test-print
```

**Reset Printed Labels**:
```bash
python main.py reset-labels
```

**Start Web Server**:
```bash
python main.py server --host 0.0.0.0 --port 5000
```

---

## 📋 Jira Ticket Workflow

1. **Export Ticket**: In Jira, go to ticket → More Actions → Export → XML
2. **Save to Directory**: Place XML file in `tickets/` directory
3. **Print**: Run `python main.py` → Option 4 → Select ticket

Ticket prints include:
- Ticket key (large header)
- Summary (bold)
- Type, Status, Priority
- Assignee
- Labels

---

## 🏷️ Large Label Printing

Create large, visible labels for Kanban lanes or sections:

1. **Interactive**: Run `python main.py` → Option 5 → Enter text
2. **Command Line**: `python main.py print-label YOUR TEXT`

**Features:**
- 7-line tall ASCII art letters
- Double-width printing for maximum visibility
- Rotated 90° to print lengthwise on paper
- Perfect for "TODO", "IN PROGRESS", "DONE" lane headers
- Supports A-Z, 0-9, and basic punctuation

**Tips:**
- Keep text under 20 characters for reasonable label length
- Use short, impactful words (TODO, BLOCKED, REVIEW)
- Labels are designed to be visible from across the room

---

## 📊 Barcode Printing

Generate and print scannable barcodes for inventory, tickets, URLs, and more:

1. **Interactive**: Run `python main.py` → Option 7 → Select type and enter data
2. **Command Line**: `python main.py barcode "YOUR DATA"`

**Supported Barcode Types:**
- **CODE128**: Most versatile, supports alphanumeric (recommended for general use)
- **CODE39**: Simple alphanumeric, widely used in logistics
- **EAN13**: 13-digit retail product codes
- **EAN8**: 8-digit compact retail codes
- **UPC-A**: 12-digit North American retail standard
- **ITF**: Interleaved 2 of 5, numeric only (shipping/warehouse)
- **CODABAR**: Numeric with special characters (libraries/blood banks)
- **CODE93**: Compact alphanumeric

**Examples:**
```bash
# General text (CODE128 default)
python main.py barcode "Hello123"

# Ticket numbers
python main.py barcode "TICKET-2024-001" --type CODE39

# Product codes
python main.py barcode "1234567890128" --type EAN13

# Custom height and width
python main.py barcode "ABC123" --height 150 --width 4

# List all supported types
python main.py barcode --list

# Show format examples
python main.py barcode --list-examples
```

**Tips:**
- Use CODE128 for general alphanumeric text (most flexible)
- EAN13/UPC-A require exact digit lengths (13 and 12 respectively)
- Increase height (50-255) for better scanability at distance
- Position option: ABOVE, BELOW, BOTH, or OFF for human-readable text

---

## 🌐 Web Server API

### POST /print
Print custom text:
## 🔧 Configuration

### Printer Connection Types

**USB Printer (Direct Connection)**:
- Ideal for single workstation setups
- Requires USB connection to computer
- Windows requires libusb driver

Configuration in `.env`:
```env
PRINTER_CONNECTION_TYPE=usb
USB_VENDOR_ID=0x0FE6
USB_PRODUCT_ID=0x811E
```

Find your USB printer IDs:
```bash
# Windows (PowerShell)
Get-PnpDevice -Class USB

# Linux/Mac
```
operation-r/
├── main.py                 # CLI entry point with interactive menu
├── setup_printer.py        # Interactive printer setup wizard
├── printer_config.py       # Printer connection abstraction (USB/network)
├── fetch_emails.py         # Gmail monitoring service
├── print_ticket.py         # Jira ticket printing from XML
├── print_label.py          # Large ASCII label printing (rotated 90°)
├── reset_printed_labels.py # Remove printed labels from emails
├── auth_gmail.py           # Gmail API authentication
├── credentials.json        # Gmail API credentials
├── .env                    # Environment configuration
├── requirements.txt        # Python dependencies
├── tickets/                # Jira XML exports
│   ├── QCLVL3-1624.xml
│   ├── QCLVL3-1637.xml
│   └── QCWEB-4613.xml
└── data/                   # Runtime data (token.json)
```d your network printer IP:
- Check printer's network settings menu
- Print network configuration page from printer
- Check your router's connected devices list
- Use printer's display panel (if available)

## 🐛 Troubleshooting

**Printer Not Found (USB)**:
- Verify USB connection and printer is powered on
- Check USB IDs match your printer (run setup wizard)
- Install libusb driver on Windows
- Try a different USB port
- Check Device Manager for USB device errors

**Printer Not Found (Network)**:
- Verify printer is powered on and connected to network
- Ping the printer IP address to test connectivity
- Check firewall isn't blocking port 9100 (or your configured port)
- Verify printer has a static IP or DHCP reservation
- Ensure printer is on the same network/VLAN
- Check printer's network settings page for correct IP

**Connection Type Issues**:
- Run `python main.py setup` to reconfigure printer
- Check `PRINTER_CONNECTION_TYPE` is set correctly in `.env`
- For USB: ensure USB_VENDOR_ID and USB_PRODUCT_ID are correct
- For network: ensure PRINTER_IP and PRINTER_PORT are correct

**Gmail Authentication**:
USB_PRODUCT_ID=0x811E
```

Find your printer IDs:
```bash
# Windows (PowerShell)
Get-PnpDevice -Class USB
```

### Text Formatting
Thermal printer uses 24-character width for optimal 80mm paper fit. Adjust in `print_ticket.py` if needed.

---

## 📁 Project Structure

```
operation-r/
├── main.py                 # CLI entry point with interactive menu
├── fetch_emails.py         # Gmail monitoring service
├── print_ticket.py         # Jira ticket printing from XML
├── print_label.py          # Large ASCII label printing (rotated 90°)
├── reset_printed_labels.py # Remove printed labels from emails
├── auth_gmail.py           # Gmail API authentication
├── credentials.json        # Gmail API credentials
├── .env                    # Environment configuration
├── requirements.txt        # Python dependencies
├── tickets/                # Jira XML exports
│   ├── QCLVL3-1624.xml
│   ├── QCLVL3-1637.xml
│   └── QCWEB-4613.xml
└── data/                   # Runtime data (token.json)
```

---

## 🐛 Troubleshooting

**Printer Not Found**:
- Verify USB connection
- Check USB IDs match your printer
- Install libusb driver (Windows)

**Gmail Authentication**:
- Ensure `credentials.json` exists
- Run `python auth_gmail.py` to authenticate
- Check `token.json` was created in `data/`

**Email Not Printing**:
- Verify email has `KanbanPrint` label in Gmail
- Check Gmail API permissions include label modification
- Review console output for errors

**Ticket Too Long**:
- Descriptions are omitted to keep printouts post-it sized
- Adjust `truncate_text()` in `print_ticket.py` if needed

---

## 📄 License

MIT License — free to use, modify, and share.
