import pandas as pd
# import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

from datetime import timedelta
from datetime import datetime
from datetime import timezone

def preprocess_data(df_):
    df_ = df_.drop_duplicates()

    # backup data
    df_backup = df_.copy()
    
    # hapus refund
    df_ = df_.drop(df_[df_['refund_status'] == 1].index)

    # choose variable
    df_finish = df_[['order_id', 'order_datetime', 'buyer_id', 'gmv', 'refund_status']]

    # Convert 'order_datetime' to datetime type
    df_finish['order_datetime'] = pd.to_datetime(df_finish['order_datetime'])

    # label encoder for buyer id
    # Membuat objek encoder
    encoder = LabelEncoder()

    # Menggunakan encoder untuk mengonversi kolom buyer_id menjadi bilangan bulat
    df_finish['buyer_id_encoded'] = encoder.fit_transform(df_finish['buyer_id']) + 1

    # Hitung variabel RFM
    snapshot_date = df_finish['order_datetime'].max() + timedelta(days=1)
    snapshot_date_str = snapshot_date.strftime('%Y-%m-%d')

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

    df_scaled = pd.DataFrame(df_scaled, columns=['Recency', 'Frequency', 'MonetaryValue', 'Length'])
    
    # Reset the index and add 1 to the index values
    df_scaled = df_scaled.reset_index(drop=True)
    df_scaled.index += 1
    print(data_lrfm)
    return data_lrfm, df_scaled

# import pickle
# def save_data_lrfm():
#     global data_lrfm

#     # Retrieve the data_lrfm from the request or any other source
#     data_lrfm = pd.DataFrame(data_lrfm, columns=['buyer_id_encoded','Recency','Frequency','MonetaryValue', 'Length'])

#     # Save data_lrfm to a file using pickle
#     with open('data_lrfm.pkl', 'wb') as f:
#         pickle.dump(data_lrfm, f)

#     return 'Data saved successfully.'