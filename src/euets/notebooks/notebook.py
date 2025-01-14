# Test to understand why we lost data
# %%
import os
import s3fs
import pandas as pd
import openpyxl

# %%
# Download installation data
# Create filesystem object

S3_ENDPOINT_URL = "https://" + os.environ["AWS_S3_ENDPOINT"]
print(S3_ENDPOINT_URL)
fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': S3_ENDPOINT_URL})
BUCKET = "jubornier/"
FILE_KEY_S3 = "/euets/installation.csv"
FILE_PATH_S3 = BUCKET + "/" + FILE_KEY_S3
with fs.open(FILE_PATH_S3, mode="rb") as file_in:
    df_insta = pd.read_csv(file_in, sep=",")

# Download account data 

S3_ENDPOINT_URL = "https://" + os.environ["AWS_S3_ENDPOINT"]
print(S3_ENDPOINT_URL)
fs = s3fs.S3FileSystem(client_kwargs={'endpoint_url': S3_ENDPOINT_URL})

FILE_KEY2_S3 = "/euets/account.csv"
FILE_PATH2_S3 = BUCKET + "/" + FILE_KEY2_S3
with fs.open(FILE_PATH2_S3, mode="rb") as file_in:
    df_acc = pd.read_csv(file_in, sep=",")


# %%
df_fr_acc = df_acc[df_acc["registry_id"] == "FR"]
print(f"Il y a {len(df_fr_acc)} entreprises française in account")
print(f"Il manque le VAT de {df_fr_acc["companyRegistrationNumber"].isna().sum()} entreprises pour la France")


# %%
df_fr_insta = df_insta[df_insta["registry_id"] == "FR"].rename(columns={"id": "installation_id"})
print(f"Il y a {len(df_fr_insta)} entreprises française in insta")
print(f"Il manque l'adresse de {df_fr_insta["addressMain"].isna().sum()} entreprise(s) française(s)")

# %%
df_fr_acc["installation_id"].equals(df_fr_insta["installation_id"])

# %%

df_fr_merge = pd.merge(df_fr_acc, df_fr_insta, on="installation_id", how="right")
df_fr_merge = df_fr_merge[["installation_id", "companyRegistrationNumber", "addressMain", "addressSecondary", "postalCode", "city", "latitudeEutl" , "longitudeEutl"]]
print(f"Il y a {len(df_fr_merge)} entreprises française une fois les deux dataset réunis")
print(f"Il manque le VAT de {df_fr_merge["companyRegistrationNumber"].isna().sum()} entreprises pour la France")
print(f"Il manque l'adresse de {df_fr_merge["addressMain"].isna().sum()} d'entreprises françaises")
# %%
df_final = df_fr_merge.dropna(subset=["companyRegistrationNumber","addressMain"])


#%%
df_final = df_final[["installation_id","companyRegistrationNumber", "addressMain", "addressSecondary", "postalCode", "city", "latitudeEutl" , "longitudeEutl"]]
# %%
print(f"Au final il y a {len(df_final)} entreprises")

# %%
df_final[df_final["addressMain"] == "-"].shape[0]

# %%
df_final[df_final["companyRegistrationNumber"] == "-"].shape[0]
df_final = df_final[df_final["addressMain"] != "-"]

# %% 
print(f"Nous avons {len(df_final)} entreprises pour la France avec Adresse et Sirene")

# %%
file_name = "EUetsfirms.xlsx"
df_final.to_excel(file_name)


# %%
df_final["companyRegistrationNumber"].tolist()
# %%
df_final["companyRegistrationNumber"].to_string("Firms_siren_list")
# %%
