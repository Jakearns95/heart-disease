"""Functions for cleansing the data files for the heart disease final project.
"""
import logging
import pandas as pd
import pickle
from pathlib import Path
import numpy as np

LOGGER = logging.getLogger(__name__)

def get_clean_df(raw_path = '',
                        clean_path="infer", 
                        use_cache=True, raw_only=False):
    """If a cached version of the cleaned file exists, it'll return 
    that (unpickled) dataframe.
    If no cached version exists, it imports and cleans the specified Heart Disease (HD) csv.  
    Args:
      * raw_path - local path to csv with claims data
      * clean_path - local path where cleaned data should be. 
        Looks there for a cached version, and saves a pkl of cleaned version there.
      * use_cache - whether the cached version should be used instead of
        rerunning the cleaning (~12 sec).
      * raw_only - disables the cleaning of the data, to just read the csv. 
        No cache is made.
      * Can specify if you want to clean out duplicates first.
    Returns: a dataframe with the cleaned (raw, if raw_only==True) HD data.
      If cleaned, it also saves a cached, pickled version of the dataframe in 
      the same location as `clean_path` with "_cleaned" postpended to the name.
    """
    raw_path = Path(raw_path)
    if (clean_path == "infer"):
        clean_path = raw_path.parent / (raw_path.stem + "_cleaned.pkl")
    clean_path = Path(clean_path)
        
    # Use cached version if one already exists
    if use_cache and clean_path.exists():
        with open(clean_path, "rb") as f:
            df = pickle.load(f)
        LOGGER.info("Using cached version of cleaned HD data")
    else:
        # Load (and optionally clean) the local csv
        header_row = ['age','sex','pain','BP','chol','fbs','ecg','maxhr','exang','eist','slope','vessels','thal','diagnosis']
        
        #define dtypes for each column
        df = pd.read_csv(raw_path, low_memory=False, encoding = 'latin-1', names = header_row,
                         error_bad_lines = False, na_values=["?"])
                        
        if raw_only:
            LOGGER.debug("Loaded input HD df, with no additional cleaning.")
        else:
            LOGGER.debug("Cleaning HD data")
            df = clean_df(df)

            # Save pickle as new cache
            with open(clean_path, 'wb') as f:
                pickle.dump(df, f)
    
    return df


def clean_df(df):
    """Cleans claims data (i.e. from `XACT_BASE.csv`).  
    Converts columns to datetime, bool and category values."""
    ans = df.copy()
    
#     # replacing ? in all columns to null
#     for col in ['BP','chol','fbs','maxhr','eiang','eist','slope','vessels','thal']:
#         ans[col] = ans[col].str.replace('?', np.nan, regex=True).astype(float)
        
    #changing dtypes over to int64
    for col in ['BP','chol','fbs','maxhr','exang','eist','slope','vessels','thal']:
        ans[col] = ans[col].astype(float)
        
    
    
    
#     # category columns
#     for col in ["LINE_CODE", "TYPE_CODE", "CONTRACT_STATE", "ENTRY_SOURCE", "TYPE_OF_LOSS", 
#                 "CLAIM_REGION", "CLAIM_BRANCH", "CLAIM_SUBBRANCH_STATE"]:
#         ans[col] = ans[col].astype("category")

#     # boolean columns
#     ans["LAST_ACTIVITY_IND"] = (ans["LAST_ACTIVITY_IND"] == "Y")
    
#     # list column
#     ans["REASSIGN_CHAIN"] = ans["REASSIGN_CHAIN"].str.split(",")

    return ans