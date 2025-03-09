import request

def get_ip_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=61439").json()
        print("\n📍 Geo-Location Data:")
        print(f"🔹 IP Address: {response.get('query', 'N/A')}")
        print(f"🔹 Country: {response.get('country', 'N/A')} ({response.get('countryCode', 'N/A')})")
        print(f"🔹 Region: {response.get('regionName', 'N/A')}")
        print(f"🔹 City: {response.get('city', 'N/A')}")
        print(f"🔹 ZIP Code: {response.get('zip', 'N/A')}")
        print(f"🔹 Latitude: {response.get('lat', 'N/A')}")
        print(f"🔹 Longitude: {response.get('lon', 'N/A')}")
        print(f"🔹 ISP: {response.get('isp', 'N/A')}")
        print(f"🔹 Timezone: {response.get('timezone', 'N/A')}")
        print(f"🔹 Autonomous System: {response.get('as', 'N/A')}")
        
    except Exception as e:
        print("Error:", e)
ip_address = input("Enter IP Address: ")
get_ip_location(ip_address)
