import requests
# pyrefly: ignore [missing-import]
from django.utils import timezone
from .models import Visitor

def get_client_ip(request):
    """
    Get the visitor's client IP address, handling potential reverse proxies/load balancers.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def fetch_ip_data(ip):
    """
    Query the IP geolocation API for the client IP.
    If the IP is local or private, falls back to a realistic mock Bangladeshi IP.
    Handles timeouts and API failures gracefully with safe defaults.
    """
    is_local = False
    
    # Check for private or loopback IPs
    if ip in ('127.0.0.1', 'localhost', '::1', '118.179.146.204') or ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.16.') or ip.startswith('169.254.'):
        is_local = True
        # Use a realistic public IP from Dhaka, Bangladesh for local testing and demo
        ip = '103.150.134.12'

    try:
        # Use ipapi.co (free tier) with a strict 2-second timeout to avoid page delays
        response = requests.get(
            f"https://ipapi.co/{ip}/json/", 
            headers={'User-Agent': 'django-visitor-tracker'}, 
            timeout=2.0
        )
        if response.status_code == 200:
            data = response.json()
            if not data.get('error'):
                # Map continent codes to complete continent names
                continent_map = {
                    'AF': 'Africa',
                    'AN': 'Antarctica',
                    'AS': 'Asia',
                    'EU': 'Europe',
                    'NA': 'North America',
                    'OC': 'Oceania',
                    'SA': 'South America'
                }
                ccode = data.get('continent_code', '')
                continent_name = continent_map.get(ccode, ccode or 'Unknown')

                return {
                    'ip': data.get('ip', ip),
                    'country': data.get('country_name', 'Bangladesh' if is_local else 'Unknown'),
                    'country_code': data.get('country_code', 'BD' if is_local else 'UN'),
                    'continent': continent_name,
                    'continent_code': ccode or ('AS' if is_local else 'UN'),
                    'city': data.get('city', 'Dhaka' if is_local else 'Unknown'),
                    'county': data.get('county') or ('Dhaka District' if is_local else ''),
                    'region': data.get('region', 'Dhaka Division' if is_local else 'Unknown'),
                    'region_code': data.get('region_code', 'C' if is_local else 'UN'),
                    'timezone': data.get('timezone', 'Asia/Dhaka' if is_local else 'UTC'),
                    'owner': data.get('org') or data.get('asn') or ('Mock ISP' if is_local else 'Unknown'),
                    'latitude': data.get('latitude', 23.8103 if is_local else 0.0),
                    'longitude': data.get('longitude', 90.4125 if is_local else 0.0),
                    'currency': data.get('currency', 'BDT' if is_local else 'USD'),
                    'languages': data.get('languages', 'bn,en' if is_local else 'en'),
                }
    except Exception as e:
        print(f"[Visitor Geolocation] Exception during external fetch: {e}")

    # Safe fallback if API call fails or times out
    return {
        'ip': ip,
        'country': 'Bangladesh' if is_local else 'Unknown',
        'country_code': 'BD' if is_local else 'UN',
        'continent': 'Asia' if is_local else 'Unknown',
        'continent_code': 'AS' if is_local else 'UN',
        'city': 'Dhaka' if is_local else 'Unknown',
        'county': 'Dhaka District' if is_local else '',
        'region': 'Dhaka Division' if is_local else 'Unknown',
        'region_code': 'C' if is_local else 'UN',
        'timezone': 'Asia/Dhaka' if is_local else 'UTC',
        'owner': 'Mock ISP' if is_local else 'Unknown',
        'latitude': 23.8103 if is_local else 0.0,
        'longitude': 90.4125 if is_local else 0.0,
        'currency': 'BDT' if is_local else 'USD',
        'languages': 'bn,en' if is_local else 'en',
    }

def record_visitor(request):
    """
    Check request parameters and record visitor IP & geodata.
    Updates the database with incremented visit count and latest timestamp.
    """
    # Skip AJAX calls or internal reloads to prevent false statistics
    if (request.headers.get('x-requested-with') == 'XMLHttpRequest' or 
        request.path.startswith('/get_') or 
        request.path.startswith('/__reload__/')):
        return

    ip = get_client_ip(request)

    try:
        # Check if visitor already exists in logs
        visitor = Visitor.objects.get(visitor_ip=ip)
        if ip != '118.179.146.204':
            visitor.visit_count += 1
            visitor.save()  # auto_now=True automatically handles visit_date update
    except Visitor.DoesNotExist:
        # Fetch geolocation details for new visitor
        geo = fetch_ip_data(ip)
        try:
            Visitor.objects.create(
                visitor_ip=ip,
                country=geo['country'],
                country_code=geo['country_code'],
                continent=geo['continent'],
                continent_code=geo['continent_code'],
                city=geo['city'],
                county=geo['county'],
                region=geo['region'],
                region_code=geo['region_code'],
                timezone=geo['timezone'],
                owner=geo['owner'],
                latitude=geo['latitude'],
                longitude=geo['longitude'],
                currency=geo['currency'],
                languages=geo['languages'],
                visit_count=1
            )
        except Exception as e:
            # Handle potential race conditions under rapid multi-requests
            print(f"[Visitor Geolocation] Failed to save new visitor: {e}")
