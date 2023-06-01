import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

from datetime import timedelta
from datetime import datetime
from datetime import timezone


# read data
df_ = pd.read_csv('/content/drive/MyDrive/Skripsi/dataset/ralali_join_2020.csv')

df_ = df_.drop_duplicates()

# backup data
df_backup = df_.copy()

# hapus refund
df_ = df_.drop(df_[df_['refund_status'] == 1].index)

# choose variable
df_finish = df_[['order_id', 'order_datetime', 'buyer_id', 'gmv', 'refund_status']]

# label encoder for buyer id
# Membuat objek encoder
encoder = LabelEncoder()

# Menggunakan encoder untuk mengonversi kolom buyer_id menjadi bilangan bulat
df_finish.loc[:, 'buyer_id_encoded'] = encoder.fit_transform(df_finish['buyer_id'])

# Hitung variabel RFM
snapshot_date = df_finish['order_datetime'].max() + timedelta(days=1)

data_lrfm = df_finish.groupby(['buyer_id_encoded']).agg({
    'order_datetime': lambda x: (snapshot_date - x.max()).days,
    'buyer_id_encoded': 'count',
    'gmv': 'sum'})

data_lrfm.rename(columns={'order_datetime': 'Recency',
                   'buyer_id_encoded': 'Frequency',
                   'gmv': 'MonetaryValue'}, inplace=True)

# Hitung variabel L
today = datetime.now(timezone.utc)
data_lrfm['Length'] = (today - df_finish.groupby(['buyer_id_encoded'])['order_datetime'].min()).dt.days

# Rescaling Atribute
rescaling_df = data_lrfm[['Recency','Frequency','MonetaryValue', 'Length']]
# Instantiate
scaler = StandardScaler()
# fit_transform
df_scaled = scaler.fit_transform(rescaling_df)
df_scaled.shape

df_scaled = pd.DataFrame(df_scaled)
df_scaled.columns = ['Recency','Frequency','MonetaryValue', 'Length']
df_scaled.head()

# df_finish = df_finish.iloc[:5000]