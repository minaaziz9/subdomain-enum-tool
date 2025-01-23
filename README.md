Subdomain Enumeration Tool
This project is a Flask-based API designed to enumerate subdomains for a given domain. It integrates with AlienVault's OTX API to fetch subdomains and provides an easy-to-use interface for integrating with frontends or other tools.

Features
Fetch subdomains for any given domain using the AlienVault OTX API.
Deduplicate and validate subdomain results.
Optional live check for subdomains using HTTP(S).
CORS support for seamless frontend integration.
Deployed on AWS Elastic Beanstalk for scalable production use.
API Endpoints
GET /subdomains
Fetch subdomains for a given domain.

Query Parameters:

domain (required): The target domain (e.g., example.com).
live (optional, default: false): Whether to perform live checks on the subdomains.
Example Request:


GET /subdomains?domain=example.com&live=true
Example Response:


{
  "domain": "example.com",
  "message": "More subdomains available, but only live subdomains are displayed.",
  "subdomains": [
    "admin.example.com",
    "mail.example.com",
    "shop.example.com"
  ]
}
Getting Started
1. Clone the Repository

git clone https://github.com/your-username/subdomain-enum-tool.git
cd subdomain-enum-tool
2. Install Dependencies
Make sure you have Python 3.8+ installed. Create a virtual environment and install the required dependencies:

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Run the Application Locally

python application.py
The application will run locally on http://127.0.0.1:5000.

4. Test the API
You can test the API using your browser or tools like Postman:

http://127.0.0.1:5000/subdomains?domain=example.com
Deployment
AWS Elastic Beanstalk
The app is configured for deployment on AWS Elastic Beanstalk. Follow these steps to deploy:

Initialize Elastic Beanstalk:

eb init
Create an Environment:

eb create subdomain-enum-env
Deploy the App:

eb deploy
AlienVault OTX API Key
Make sure to replace the placeholder in the code with your actual OTX API Key:

API_KEY = "your-otx-api-key"
Project Structure

subdomain-enum-tool/
├── application.py        # Main Flask application
├── requirements.txt      # Python dependencies
├── .ebextensions/        # Elastic Beanstalk configuration
│   └── scripts.config    # Scripts to install dependencies
├── README.md             # Project documentation
Configuration
Environment Variables
Set the following environment variables for secure configuration:

OTX_API_KEY: Your AlienVault OTX API key.
Modify Configuration
Update application.py to reflect any custom API keys or endpoints.
Known Limitations
Rate Limiting: AlienVault OTX may rate-limit excessive requests.
Live Check: Live checking of subdomains may increase response times.
Future Enhancements
Add support for additional subdomain enumeration APIs (e.g., SecurityTrails, Shodan).
Implement caching to reduce redundant API requests.
Improve error handling and logging.
License
This project is licensed under the MIT License.

Contributions
Contributions are welcome! Feel free to submit issues or pull requests to improve the tool.

Contact
Author: Mina Aziz
For any questions, feel free to reach out at your-email@example.com.
