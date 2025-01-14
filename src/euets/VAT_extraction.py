import pandas as pd
from download_ssp_cloud import download_data_acc, download_data_insta

df_euets_account = download_data_acc()
df_euets_insta = download_data_insta()

print(len(df_euets_account))
print(len(df_euets_insta))

# Account data
# VAT = TVA intercommunautaire (équivalent siret)
# dans la doc : VAT registration number of the associated company

df_euets_account["companyRegistrationNumber"]
df_euets_account_fr = df_euets_account[df_euets_account["registry_id"] == "FR"]

# Pour la france registration number = Siren (test CPTE POLYREY sur Insee)
# BvdId des entreprises = FR(ISO2)+ Siren  <=> ORBIS identifier (https://login.bvdinfo.com/R1/Orbis)
test_df = df_euets_account[df_euets_account["accountIDTransactions"] =="FR_479"]
print(test_df.head())

# Missing VA Id
account_na = df_euets_account_fr["installation_id"].isna().sum()
account_len = len(df_euets_account_fr)
miss_id = (account_na/account_len)*100 
print(f"Il manque {miss_id} % des données pour l'id installation en France")

# accountIDTransactions to merge account & installation

id_transa_na = df_euets_account_fr["accountIDTransactions"].isna().sum()
id_transa_len = len(df_euets_account)
miss_id_tran = (id_transa_na/id_transa_len)*100
print(f"Il manque {miss_id_tran} % des identifiants des comptes")


# Installation data
df_geo = df_euets_insta[["id", "registry_id", "tradingSystem_id", "addressMain", "addressSecondary", "postalCode", "city", "latitudeEutl" , "longitudeEutl"]].rename(columns= {"id" : "accountIDTransactions"})

df_geo_fr = df_geo[df_geo["registry_id"] == "FR"]

geo_na = df_geo_fr["addressMain"].isna().sum()
geo_len = len(df_geo_fr["addressMain"])
miss = (geo_na/geo_len)*100
print(f"Il manque {miss} % des adresses")

# Merger les deux dataframes
df_merge = pd.merge(df_euets_account_fr, df_geo_fr, on="accountIDTransactions", how="right")

adress_na = df_merge["addressMain"].isna().sum()
merge_len = len(df_merge)
miss_address = (adress_na/merge_len)*100
print(f"Il y a {merge_len} entreprises")
print(f"Il manque {miss_address}% des adresses")

df_euets = df_merge[["accountIDTransactions","companyRegistrationNumber", "addressMain", "addressSecondary", "postalCode", "city", "latitudeEutl" , "longitudeEutl"]]

df_euets_final = df_euets.dropna(subset=["companyRegistrationNumber"])
dim_euest = len(df_euets_final)
print(f"Il reste {dim_euest} entreprises avec Siren ou Siret & adresses")

