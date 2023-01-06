"""
Testing Google Storage.

Bash syntax:

    ```bash
    PROJECT_ID="curious-entropy-199817"
    BUCKET="$PROJECT_ID-test-bucket-1"
    echo "Hello world at `date`" > test.txt

    # Upload two files.
    gcloud storage cp test.txt gs://$BUCKET/prefix-1/prefix-2/prefix-3/test.txt
    gcloud storage cp test.txt gs://$BUCKET/prefix-1/prefix-2/prefix-4/test.txt

    # Move file.
    gcloud storage mv gs://$BUCKET/prefix-1/prefix-2/prefix-4/test.txt gs://$BUCKET/prefix-1/prefix-2/prefix-5/test.txt

    # Query all files at prefix.
    gcloud storage ls gs://$BUCKET/prefix-1/**/*
    gcloud storage ls --recursive gs://$BUCKET/prefix-1

    # Download all files at prefix.
    gcloud storage cp --recursive gs://$BUCKET/prefix-1 .

    # Delete all files at prefix.
    gcloud storage rm --recursive gs://$BUCKET/prefix-1
    ```

References:
    - `gcloud storage` command
      https://cloud.google.com/sdk/gcloud/reference/storage

    - Download objects as files:
      https://cloud.google.com/storage/docs/downloading-objects

    - Upload objects from files:
      https://cloud.google.com/storage/docs/uploading-objects

    - Copy, rename, and move objects:
      https://cloud.google.com/storage/docs/copying-renaming-moving-objects
"""
import json
from pathlib import Path
from typing import List
from google.cloud import storage
from google.oauth2.service_account import Credentials



class Config:
    """Contains input variables and config."""
    def __init__(self):
        self.project_id: str = 'curious-entropy-199817'
        self.bucket: str = f'{self.project_id}-test-bucket-1'
        self.creds_file: Path = Path(__file__).parents[1] / 'infra' / 'test_service_account' / 'key.json'
        self.creds: Credentials = Credentials.from_service_account_file(self.creds_file)


def create_files() -> List[Path]:
    """Creates N local files."""
    return [create_file(i) for i in range(3)]


def create_file(i: int) -> Path:
    """Creates a local file."""
    data = {'index': i, 'message': f'Hello world {i}!'}
    path = Path.cwd() / f'test{i}.json'
    with open(path, 'w') as file:
        json.dump(data, file)
    return path


def upload_files(bucket: storage.Bucket, paths: List[Path]):
    """Uploads files to cloud storage."""
    for local_path in paths:
        blob = bucket.blob(f'prefix-1/prefix-2/prefix-3/{local_path.name}')
        print(f'Uploading to:  {blob.name}.')
        blob.upload_from_filename(local_path)


def delete_files(bucket: storage.Bucket, paths: List[Path]):
    """Deletes files from cloud storage."""
    for local_path in paths:
        blob = bucket.blob(f'prefix-1/prefix-2/prefix-3/{local_path.name}')
        print(f'Deleting:  {blob.name}.')
        blob.delete()
        local_path.unlink()



if __name__ == '__main__':
    print('Begin.')
    config = Config()
    client = storage.Client(credentials=config.creds)
    bucket = client.bucket(config.bucket)
    paths = create_files()
    upload_files(bucket, paths)
    delete_files(bucket, paths)
    # TODO:  Test move, copy, download, etc.
    print('Done.')
