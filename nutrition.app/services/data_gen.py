import pandas as pd

def generate_nutrition_data(days: int = 7) -> pd.DataFrame:
    """
    Generates a simulated nutrition dataset.
    
    :param days: Number of days to simulate
    :return: Pandas DataFrame with nutrition data
    """
    
    data = {
        "Day": list(range(1, days + 1)),
        "Calories": [2200, 2100, 2500, 2300, 2000, 2400, 2150][:days],
        "Protein": [120, 110, 130, 125, 100, 140, 115][:days],
    }
    
    return pd.DataFrame(data)