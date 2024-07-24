from argparse import ArgumentParser
from datetime import datetime

def main():
    parser = ArgumentParser(prog='cli')

    parser.add_argument('--access-token', type=str, required=True, help='Your Facebook Graph API access token')
    parser.add_argument('--start-date', type=str, required=True, help='Start date for scraping (format: YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, required=True, help='End date for scraping (format: YYYY-MM-DD)')

    args = parser.parse_args()

    args = parser.parse_args()

    # Validate date format
    try:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
    except ValueError:
        print("Error: Dates must be in YYYY-MM-DD format.")
        return

    # Print arguments (for testing purposes)
    print(f"Access Token: {args.access_token}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")


if __name__ == '__main__':
    main()
