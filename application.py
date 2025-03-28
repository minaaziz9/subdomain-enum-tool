from flask import Flask, request, jsonify
import httpx
import re
from flask_cors import CORS

application = Flask(__name__)
CORS(application)

API_KEY = "2508a1a605ba0ff16c1d060870a406fe315d714fb1c85fee88a59dfe231d9c89"  # Replace with your actual AlienVault OTX API key

@application.route('/subdomains', methods=['GET'])
def fetch_subdomains():
    domain = request.args.get('domain')
    include_live_check = request.args.get('live', 'false').lower() == 'true'

    if not domain:
        return jsonify({"error": "Domain parameter is required."}), 400

    try:
        subdomains = query_alienvault(domain)
        subdomains = list(set(filter_valid_subdomains(subdomains)))  # Deduplicate and filter

        if not subdomains:
            return jsonify({"domain": domain, "message": "No subdomains found.", "subdomains": []}), 200

        # Limit to the first 25 fetched subdomains
        subdomains = subdomains[:25]
        has_more = len(subdomains) > 10

        if include_live_check:
            live_subdomains = check_live_subdomains(subdomains)  # Check all 25 subdomains for live status
            live_subdomains_limited = live_subdomains[:10]  # Display only the first 10 live subdomains
        else:
            live_subdomains_limited = subdomains[:10]

        return jsonify({
            "domain": domain,
            "subdomains": live_subdomains_limited,
            "message": "More subdomains available, but only live subdomains are displayed." if has_more else None
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def query_alienvault(domain):
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
    headers = {"X-OTX-API-KEY": API_KEY}

    try:
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except httpx.RequestError as e:
        raise Exception(f"Failed to fetch data from AlienVault OTX: {str(e)}")

    try:
        data = response.json()
        subdomains = [record['hostname'] for record in data.get('passive_dns', [])]
        return subdomains
    except Exception as e:
        raise Exception(f"Error parsing AlienVault OTX response: {str(e)}")


def filter_valid_subdomains(subdomains):
    valid_subdomains = []
    domain_regex = re.compile(r'^(?!\*\.)(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')

    for sub in subdomains:
        sub = sub.strip()
        if domain_regex.match(sub):
            valid_subdomains.append(sub)

    return valid_subdomains


def check_live_subdomains(subdomains):
    live_subdomains = []
    for sub in subdomains:
        try:
            response = httpx.get(f"https://{sub}", timeout=5)  # Use HTTPS for live check
            if response.status_code < 400:  # Treat 200-399 as live
                live_subdomains.append(sub)
        except httpx.RequestError:
            continue  # Skip if the subdomain is not reachable
    return live_subdomains

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(debug=True, host='0.0.0.0', port=port)
