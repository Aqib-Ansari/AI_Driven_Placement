from google.cloud import storage

def upload_to_firebase(file_path, destination_path, project_id):
    client = storage.Client(project=project_id)
    bucket = client.bucket('aidriven-cffe9.appspot.com')  # Replace with your Firebase Storage bucket name

    blob = bucket.blob(destination_path)
    blob.upload_from_filename(file_path)

    print(f"File {file_path} uploaded to {destination_path} in Firebase Storage.")

# Example usage:
# file_path = "static/favicon.png"
# destination_path = "uploads/favicon.png"
# project_id = "aidriven-cffe9"

# upload_to_firebase(file_path, destination_path, project_id)


def download_from_firebase(source_path, destination_path, project_id):
    client = storage.Client(project=project_id)
    bucket = client.bucket('aidriven-cffe9.appspot.com')  # Replace with your Firebase Storage bucket name

    blob = bucket.blob(source_path)
    blob.download_to_filename(destination_path)

    print(f"File downloaded from {source_path} to {destination_path}.")

# Example usage:
source_path = "uploads/favicon.png"  # Replace with the path in Firebase Storage
destination_path = "static/favicon.png"  # Replace with the local destination path
project_id = "aidriven-cffe9"  # Replace with your Firebase project ID

download_from_firebase(source_path, destination_path, project_id)