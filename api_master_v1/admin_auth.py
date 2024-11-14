import argparse
import requests
from datetime import datetime

def consume_flask_endpoint(heading, sub_heading, created_at, item_media_plate_url, download_location):
    url = 'http://localhost:5009/request_auth_card'  # Replace with the actual endpoint URL

    # Prepare the data to send in the request
    data = {
        'heading': heading,
        'sub_heading': sub_heading,
        'created_at': created_at,
        'item_media_plate_url': item_media_plate_url
    }

    # Send a POST request to the Flask endpoint
    response = requests.post(url, data=data)

    if response.status_code == 200:
        # Save the received image file
        filename = response.headers.get('Content-Disposition').split('=')[1]
        if not download_location:
            download_location = './' + filename
        with open(download_location, 'wb') as f:
            f.write(response.content)
        print('Ticket image saved successfully.')
        print('Download location:', download_location)
    else:
        error_message = response.json().get('message', 'Failed to generate ticket image.')
        print('Error:', error_message)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client for Flask endpoint')
    parser.add_argument('--heading', help='Ticket heading')
    parser.add_argument('--sub-heading', help='Ticket subheading')
    parser.add_argument('--created-at', help='Ticket created date (default: current time)', default=str(datetime.now()))
    parser.add_argument('--plate-url', help='Path to plate image URL')
    parser.add_argument('--download-location', help='Download location (optional)')

    args = parser.parse_args()

    if args.heading and args.sub_heading and args.plate_url:
        consume_flask_endpoint(args.heading, args.sub_heading, args.created_at, args.plate_url, args.download_location)
    else:
        # Run in interactive session
        heading = input('Enter ticket heading: ')
        sub_heading = input('Enter ticket subheading: ')
        created_at = input('Enter ticket created date (default: current time): ')
        if not created_at:
            created_at = str(datetime.now())
        plate_url = input('Enter path to plate image URL: ')
        download_location = input('Enter download location (default: current directory): ')

        consume_flask_endpoint(heading, sub_heading, created_at, plate_url, download_location)
