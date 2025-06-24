import requests

# Admin panels and sensitive files to check
paths = [
    "admin", "login", "dashboard", ".env", ".git", "config.php",
    "phpinfo.php", "robots.txt", "backup.zip"
]

# Basic XSS test payload
xss_payload = "<script>alert(1)</script>"

# Security headers to check
security_headers = [
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Strict-Transport-Security",
    "X-XSS-Protection"
]

def check_common_paths(url):
    print("\n🔍 Scanning common paths and sensitive files...\n")
    for path in paths:
        target = url.rstrip("/") + "/" + path
        try:
            res = requests.get(target, timeout=5)
            if res.status_code == 200:
                print(f"[⚠️] Found: {target} (Status: 200)")
            elif res.status_code == 403:
                print(f"[🔒] Forbidden: {target} (Status: 403)")
        except:
            continue

def test_basic_xss(url):
    print("\n🧪 Testing basic XSS injection...\n")
    try:
        test_url = url + "?q=" + xss_payload
        res = requests.get(test_url, timeout=5)
        if xss_payload in res.text:
            print(f"[🚨] Possible XSS found at: {test_url}")
        else:
            print("[✅] No XSS detected.")
    except:
        print("[❌] XSS test failed.")

def check_security_headers(url):
    print("\n🔐 Checking missing security headers...\n")
    try:
        res = requests.get(url, timeout=5)
        headers = res.headers
        for header in security_headers:
            if header not in headers:
                print(f"[⚠️] Missing: {header}")
            else:
                print(f"[✅] Present: {header}")
    except:
        print("[❌] Failed to retrieve headers.")

if __name__ == "__main__":
    target_url = input("🌐 Enter the target URL (e.g. https://example.com):\n> ").strip()
    
    check_common_paths(target_url)
    test_basic_xss(target_url)
    check_security_headers(target_url)

    print("\n✅ Scan completed.")