from google.cloud import storage

def upload_file_to_firebase(file_path, destination_path, project_id):
    client = storage.Client(project=project_id)
    bucket = client.bucket('aidriven-cffe9.appspot.com')  # Replace with your Firebase Storage bucket name

    blob = bucket.blob(destination_path)
    blob.upload_from_filename(file_path)

    print(f"File {file_path} uploaded to {destination_path} in Firebase Storage.")


def download_file_from_firebase(source_path, destination_path, project_id):
    client = storage.Client(project=project_id)
    bucket = client.bucket('aidriven-cffe9.appspot.com')  # Replace with your Firebase Storage bucket name

    blob = bucket.blob(source_path)
    blob.download_to_filename(destination_path)

    print(f"File downloaded from {source_path} to {destination_path}.")



if __name__ == "__main__":

    source_path = "uploads/favicon.png"  
    destination_path = "static/favicon.png"  
    project_id = "aidriven-cffe9"  
    download_file_from_firebase(source_path, destination_path, project_id)
    
    file_path = "static/favicon.png"
    destination_path = "uploads/favicon.png"
    project_id = "aidriven-cffe9"
    upload_file_to_firebase(file_path, destination_path, project_id)