## https://pypi.org/project/paho-mqtt/
import pandas as pd
from sklearn.utils import resample


# Get dataset
raw_data = pd.read_csv('dataset_MP.csv', index_col=False)
df_majority = raw_data[(raw_data['Machine failure']==0)] 
df_minority = raw_data[(raw_data['Machine failure']==1)] 

# upsample minority class
df_minority_upsampled = resample(df_minority, 
                                 replace=True,    # sample with replacement
                                 n_samples= 9661, # to match majority class
                                 random_state=42)  # reproducible results
# Combine majority class with upsampled minority class
raw_data = pd.concat([df_minority_upsampled, df_majority])

raw_data = raw_data.sample(frac=1).reset_index(drop=True)

raw_data.to_csv("resamples_dataset.csv", index=False)