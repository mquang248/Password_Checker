# Password Strength Analyzer

A comprehensive web application for analyzing password strength and simulating ethical password cracking attempts.

## Link Test
'https://pass-checker.onrender.com'

## Features

- Real-time password strength evaluation
- Multiple criteria assessment:
  - Length check
  - Character variety
  - Common patterns detection
  - Entropy calculation
- Password cracking simulation using John the Ripper
- Beautiful and responsive web interface
- Detailed feedback and suggestions

## Tech Stack

- Python 3.11+
- Flask
- zxcvbn (Password strength estimation)
- John the Ripper (Password cracking simulation)
- Bootstrap 5 (UI Framework)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mquang248/Password_Checker.git
cd Password_Checker
```


2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install John the Ripper:
```bash
# For Debian/Ubuntu-based systems:
sudo apt-get install john
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

## Security Notice

This tool is intended for educational and security assessment purposes only. Do not use it for unauthorized password cracking or malicious purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
