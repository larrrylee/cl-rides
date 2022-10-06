import pandas as pd
import rides_data as data


def assign(df: pd.DataFrame, rf: pd.DataFrame) -> pd.DataFrame:
    assignments_df = pd.concat([pd.DataFrame(columns=[data.OUTPUT_DRIVER_NAME_KEY, data.OUTPUT_DRIVER_PHONE_KEY]), rf[[data.RIDER_NAME_KEY, data.RIDER_PHONE_KEY, data.RIDER_LOCATION_KEY, data.RIDER_NOTES_KEY]]], axis='columns')
    
    assignments_df.sort_values(by=data.OUTPUT_DRIVER_NAME_KEY)
    return assignments_df