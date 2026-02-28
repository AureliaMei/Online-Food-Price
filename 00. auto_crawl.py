import requests
import subprocess
from datetime import datetime

# --- CONFIGURATION ---
BASE_URL = "http://localhost:8080/storage/runs"

# Use the Cookie exactly as found in your Inspect tab
HEADERS = {
    "Cookie": "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiaWF0IjoxNzY5OTMxNjYwfQ.u8-oyELT3dsXusM0pBRkuQLIC8XI3mCvJW6omYa4sKk",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

ROBOTS = {
    "Electronics": "2b41463d-c127-4a97-b7f7-9f9dd1b07374",
    "Hygene": "3f88e569-057e-4319-892f-834416e6188d",
    "Dry_Food": "0ef9789a-f778-418d-8bd5-6c8b83a11286",
    "Instant_food": "f2a242f9-8a04-4cce-a5c6-2f11eda952b7", #actually Confectionary
    "Non-alcohol_beverage": "191f10fe-1d04-49e0-b3e4-fc5a4fc4b90b",
    "Household_good": "06165882-777a-4c19-8862-de530d54373d",
    "Baby_product": "62a10810-19db-4076-86af-169320baf441",
    "Egg_and_soy": "809764ec-5e4c-4eb9-aad6-cc809430648b",
    "Frozen": "70404316-22f8-4e52-a3a0-c60b302a482e",
    "Spice": "4e4a60d2-68b3-4f41-a3a0-80fdd3783c45",
    "Processed_food": "afa4380e-7f1f-4a4e-b005-746c5e7fa38d",
    "Dairy": "95087cc5-1cfb-4d58-b66b-d2356b4e5b84",
    "Confectionary": "f9a623b7-e75e-416f-aeb6-9769c9a84cc8", #non-responding
    "Detergent": "6479ca88-3fae-434d-8874-ec2e407e37ee",
    "Veg_Fruit": "424e50fb-43a0-4417-a5b7-b0ecc72597ed",
    "Actual Instant Food": "5a5c5856-ab1b-4133-a0de-148cf0837f92",
    "Alcohol": "701ec6ba-8558-4421-8c83-916681d0967c"
}

def notify_mac(title, message):
    subprocess.run(["osascript", "-e", f'display notification "{message}" with title "{title}"'])

def trigger_all_robots():
    print(f"🚀 Triggering 15 robots at {datetime.now().strftime('%H:%M:%S')}...")
    success_count = 0
    
    for name, r_id in ROBOTS.items():
        url = f"{BASE_URL}/{r_id}"
        try:
            # Note: We are now using PUT + Cookie Auth
            response = requests.put(url, headers=HEADERS)
            
            if response.status_code in [200, 204]:
                print(f"  ✅ {name:20} | Success")
                success_count += 1
            else:
                print(f"  ❌ {name:20} | Failed ({response.status_code})")
        except Exception as e:
            print(f"  ⚠️  {name:20} | Error: {e}")

    summary = f"Triggered {success_count}/{len(ROBOTS)} robots."
    notify_mac("Maxun Update", summary)

if __name__ == "__main__":
    trigger_all_robots()