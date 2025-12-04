# RED-CROSS-project
Inspired by geowifi and other awesome tools, this tools is information gathering and tracker tools specifically made for pentester and security researcher

    ██████╗ ███████╗██████╗        ██████╗██████╗  ██████╗ ███████╗███████╗
    ██╔══██╗██╔════╝██╔══██╗      ██╔════╝██╔══██╗██╔═══██╗██╔════╝██╔════╝
    ██████╔╝█████╗  ██║  ██║█████╗██║     ██████╔╝██║   ██║███████╗███████╗
    ██╔══██╗██╔══╝  ██║  ██║╚════╝██║     ██╔══██╗██║   ██║╚════██║╚════██║
    ██║  ██║███████╗██████╔╝      ╚██████╗██║  ██║╚██████╔╝███████║███████║
    ╚═╝  ╚═╝╚══════╝╚═════╝        ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝

                    |            v2.1
                 ---|---          your friendly little stalker 
            ─────┤  +  ├─────
                 ---|---
                    |

Select Attack Mode:

  [1] Basic      - Simple redirect tracking
  
  [2] Advanced   - Device fingerprint + geolocation
  
  [3] Stealth    - Mimics legitimate URL shortener
  
  [4] Ghost      - Zero footprint iframe injection
  
  [5] List       - Show all campaigns
  
  [0] Exit

# Red-Cross Link Tracker

Educational red team link tracking framework for authorized security training.

## Installation

### Using pipx (Recommended)
```bash
pipx install git+https://github.com/Wangsa779/RED-CROSS-project.git
```

### From source
```bash
git clone https://github.com/Wangsa779/RED-CROSS-project.git
cd redcross
pipx install .
```

### Traditional pip
```bash
pip install git+https://github.com/Wangsa779/RED-CROSS-project.git
```

## Usage

After installation, run from anywhere:
```bash
# Interactive mode
redcross

# Command line mode
redcross -h
redcross -g -u https://tiktok.com/@user/video/123 -c test1
```

## Modes

- **Basic**: Simple redirect tracking
- **Advanced**: Device fingerprinting + geolocation
- **Stealth**: Mimics URL shorteners
- **Ghost**: Zero footprint iframe injection

## Requirements

- Python 3.7+
- Authorized use only
- Isolated VM environment required

## Warning

⚠️ This tool is for authorized security training and red team exercises only.
Unauthorized use may violate laws and regulations.
"""

