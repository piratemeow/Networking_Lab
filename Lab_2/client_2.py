import requests
import os
SERVER_URL = "http://10.33.2.90:8080"


def download_file():
    global SERVER_URL
    response = requests.get(f"{SERVER_URL}{DOWNLOAD_PATH}")
    try:
        response.raise_for_status()  

        
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            filename = content_disposition.split("filename=")[-1].strip('"')
        else:
           
            filename = "downloaded_file.txt"

        with open(filename, "wb") as file:
            file.write(response.content)

        print(f"File '{filename}' downloaded successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download file. Error: {e}")

def upload_file():
    UPLOAD_PATH = input("Write the path of the file to be uploaded: ")

    if not os.path.exists(UPLOAD_PATH) or not os.path.isfile(UPLOAD_PATH):
        print("Invalid FIle")
        return 
    files = {'file': (os.path.basename(UPLOAD_PATH),open(UPLOAD_PATH,'rb'))}
    
    response = requests.post(f"{SERVER_URL}/home/student/Screenshots/", files=files)

    if response.status_code == 200:
        print("File uploaded successfully.")
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")


while True:
    print("Choose an option:")
    print("1. Download file")
    print("2. Upload file")
    print("3. Quit")
    DOWNLOAD_PATH="/"

    option = input("Enter your choice (1/2/3): ")

    if option == "1":
        DOWNLOAD_PATH += input("provide a path ")
        download_file()
    elif option == "2":
        upload_file()
    elif option == "3":
        break
    else:
        print("Invalid option. Please choose again.")
