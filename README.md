# 🖨️ Operation R: Email & Jira Task Printing for Kanban

**Operation R** is a robust CLI tool that automates printing emails and Jira tickets to a thermal printer for physical Kanban task management. Turn digital tasks into tangible post-it note sized printouts!

---

## ✨ Features

- 📨 **Gmail Integration**: Automatically monitor and print emails labeled with `KanbanPrint`
- 🎫 **Jira Ticket Printing**: Print Jira tickets from XML exports with clean, readable formatting
- 🖨️ **Thermal Printer Support**: Uses `python-escpos` for Rongta RP332 (80mm paper)
- 🎛️ **Interactive CLI Menu**: User-friendly numbered menu for all operations
- 🏷️ **Smart Label Management**: Tracks printed emails to avoid duplicates
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
| Hardware       | Rongta RP332 (USB)  |
| Platform       | Windows 11          |

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

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

Required settings:
- `USB_VENDOR_ID`: Printer USB vendor ID (default: 0x0FE6)
- `USB_PRODUCT_ID`: Printer USB product ID (default: 0x811E)
- `ATLASSIAN_CLOUD_ID`: Your Jira cloud instance ID

### 5. Gmail API Setup
1. Enable Gmail API in Google Cloud Console
2. Download `credentials.json` to project root
3. Run authentication: `python auth_gmail.py`

### 6. Install USB Driver (Windows)
Download libusb from: https://github.com/libusb/libusb/releases
Extract `libusb-1.0.dll` to `C:\Windows\System32`

---

## 🚀 Usage

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
3. Test print (verify printer setup)
4. Print ticket (from XML)
5. Start web server
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

## 🌐 Web Server API

### POST /print
Print custom text:
```bash
curl -X POST http://localhost:5000/print \
  -H "Content-Type: application/json" \
  -d '{"text": "Custom task description"}'
```

### POST /jira-webhook
Jira webhook endpoint (for future automation).

---

## 🔧 Configuration

### Printer Settings
Edit `.env` to match your printer:
```env
USB_VENDOR_ID=0x0FE6
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
