API_KEY = "PUT YOUR APY KEY HERE"

INPUT_FILE = "ips.txt"
ABUSEIPDB_API_URL = "https://api.abuseipdb.com/api/v2/check"

# Argument parser
parser = argparse.ArgumentParser(description="Process IPs with AbuseIPDB API")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# Resolve AbuseIPDB IP once
try:
    abuseipdb_ip = socket.gethostbyname("api.abuseipdb.com")
    if args.verbose:
        print(f"Resolved abuseipdb.com to {abuseipdb_ip}")
except socket.gaierror:
    print("Error: Unable to resolve abuseipdb.com")
    exit(1)

def query_abuseipdb(ip):
    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90,
        "verbose": True
    }
    try:
        if args.verbose:
            print(f"Querying AbuseIPDB for {ip}...")
        response = requests.get(ABUSEIPDB_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()["data"]
        return f"{ip},{data['abuseConfidenceScore']},{data['domain']},{data['countryCode']},{';'.join(data['hostnames'])}", data['abuseConfidenceScore']
    except requests.RequestException as e:
        print(f"Error querying AbuseIPDB for {ip}: {e}")
        return None, 0

def process_ips():
    processed_ips = set()
    updated_lines = []
    scored_lines = []
    
    with open(INPUT_FILE, "r") as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        match = re.match(r"^(\d+\.\d+\.\d+\.\d+)$", line)
        if match:
            ip = match.group(1)
            if ip in processed_ips:
                if args.verbose:
                    print(f"Skipping duplicate IP: {ip}")
                continue  # Skip duplicate IPs
            processed_ips.add(ip)
            new_line, score = query_abuseipdb(ip)
            if new_line:
                scored_lines.append((score, new_line))
                if args.verbose:
                    print(f"Processed {ip}: {new_line}")
        else:
            scored_lines.append((0, line))  # Keep already processed lines with default score
    
    # Sort lines by abuseConfidenceScore (ascending order, most dangerous at the end)
    scored_lines.sort(key=lambda x: x[0])
    
    with open(INPUT_FILE, "w") as file:
        file.write("\n".join([line for _, line in scored_lines]) + "\n")
    
    if args.verbose:
        print("File updated and sorted successfully.")

if __name__ == "__main__":
    process_ips()
    print("Processing complete.")

