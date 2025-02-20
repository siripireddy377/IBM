import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Carbon emission factors (kg CO₂ per unit)
ELECTRICITY_FACTOR = 0.5  # kg CO₂ per kWh
TRAVEL_FACTOR = 0.15  # kg CO₂ per km
WASTE_FACTOR = 1.2  # kg CO₂ per kg
WATER_FACTOR = 0.001  # kg CO₂ per liter

def calculate_office_footprint(electricity_usage, business_travel, office_waste, water_consumption):
    """
    Calculate the total office carbon footprint based on different factors.
    
    Parameters:
    - electricity_usage (float): Monthly electricity usage in kWh.
    - business_travel (float): Distance traveled for business in km.
    - office_waste (float): Office waste generated in kg.
    - water_consumption (float): Monthly water consumption in liters.

    Returns:
    - float: Total carbon footprint in kg CO₂.
    """

    # Validate input values
    if any(value < 0 for value in [electricity_usage, business_travel, office_waste, water_consumption]):
        logging.error("Negative input values are not allowed.")
        raise ValueError("All input values must be non-negative.")

    # Calculate emissions
    electricity_emissions = electricity_usage * ELECTRICITY_FACTOR
    travel_emissions = business_travel * TRAVEL_FACTOR
    waste_emissions = office_waste * WASTE_FACTOR
    water_emissions = water_consumption * WATER_FACTOR

    total_emissions = electricity_emissions + travel_emissions + waste_emissions + water_emissions
    
    logging.info(f"Total emissions calculated: {total_emissions:.2f} kg CO₂")
    
    return total_emissions
