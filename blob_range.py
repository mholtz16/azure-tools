import requests  # Library to make HTTP requests
import time  # Library to track execution time

# Define the chunk size for downloading in bytes (2MB per chunk)
chunk_size = 2097152  

# List of URLs to download data from (currently empty, replace with actual URLs)
urls = ['', '']

# Iterate over each URL in the list
for url in urls:
    start_time = time.time()  # Record the start time for performance tracking
    start = 0  # Initialize the starting byte position for range-based requests

    # Define the request headers to fetch the first chunk
    headers = {
        'Range': f'bytes={start}-{start+chunk_size-1}',  # Request a specific byte range
        'Accept-Encoding': 'gzip'  # Request gzip compression if available
    }

    print(headers)  # Print the headers for debugging

    # Make the first request to fetch the initial chunk of data
    response = requests.get(url, headers=headers)

    # Continue fetching more chunks while the server responds with "206 Partial Content"
    while response.status_code == 206:  
        start += chunk_size  # Move to the next chunk
        headers = {
            'Range': f'bytes={start}-{start+chunk_size-1}',  # Update the byte range for the next request
            'Accept-Encoding': 'gzip'  # Maintain gzip encoding preference
        }

        # Request the next chunk of the file
        response = requests.get(url, headers=headers)
        
        # Print the response headers for debugging
        print(response.headers)

    end_time = time.time()  # Record the end time after downloading is complete

    # Print the total duration taken for downloading the file
    print(f'Duration for {url}:\n{end_time - start_time}')