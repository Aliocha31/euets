#How to download data from S3 Bucket (from SSP cloud doc )
import os
import s3fs
import pandas as pd

# Create filesystem object
def download_data():
    S3_ENDPOINT_URL = "https://" + os.environ["AWS_S3_ENDPOINT"]
    print(S3_ENDPOINT_URL)
    fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': S3_ENDPOINT_URL})

    BUCKET = "jubornier/"
    FILE_KEY_S3 = "/euets/installation.csv"
    FILE_PATH_S3 = BUCKET + "/" + FILE_KEY_S3

    with fs.open(FILE_PATH_S3, mode="rb") as file_in:
        df_insta = pd.read_csv(file_in, sep=",")


    FILE_KEY2_S3 = "/euets/account.csv"
    FILE_PATH2_S3 = BUCKET + "/" + FILE_KEY2_S3

    with fs.open(FILE_PATH2_S3, mode="rb") as file_in:
        df_acc = pd.read_csv(file_in, sep=",")
    
    return df_acc, df_insta