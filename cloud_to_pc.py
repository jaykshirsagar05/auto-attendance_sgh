
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('autoattendance-91502-firebase-adminsdk-f7igv-441ea74b8f.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'autoattendance-91502.appspot.com'
})
# The “folder” where the files you want to download are
folder='/google-cloud/download'
delimiter='/'
bucket=storage.bucket()
blobs=bucket.list_blobs(delimiter=delimiter) #List all objects that satisfy the filter.

# Download the file to a destination
def download_to_local():

     # Create this folder locally if not exists
     if not os.path.exists(folder):
        os.makedirs(folder)
     # Iterating through for loop one by one using API call
     for blob in blobs:

         destination_uri = '{}/{}.jpg'.format(folder, blob.name)
         blob.download_to_filename(destination_uri)
         print('Exported {} to {}'.format(
         blob.name, destination_uri))
         blob_name = blob.name

         # delete the blob
         blob.delete()

         print("Blob {} deleted.".format(blob_name))


if __name__ == '__main__':
    download_to_local()
