#Riley Becker En1, Prof Carlson
# 12/16/24
#This program will calculate an amount of water and protein powder necessary to add based on a user's specific weight


#200 lbs -> 75 g of protein (World Health Org safe lower limit)
#That's 3/8 g protein / lb of weight

#Variables stored here:
UPPER_LIMIT_WATER = 500 #This is the upper limit of water (As an example)
powder_conversion = 3.0/8.0 #3/8 g protein / lb of weight is the recommended amount
water_conversion = 20.0/3.0 #Check the type of powder for exact conversion (For this example, we'll use 20g water / 3 g protein)

#Functions
def calculate_protein():
    print("Enter your weight (in lbs):")
    weight = float(input())
    if weight*powder_conversion*water_conversion > UPPER_LIMIT_WATER: #If the amount of powder exeeds the max the cup can hold
        return UPPER_LIMIT_WATER*1.0/water_conversion
    return weight*1.0*(powder_conversion)
    
def calculate_water(grams_protein):
    #1g of water = 1 mL
    return grams_protein*1.0*(water_conversion)
    
grams_protein = calculate_protein()
grams_water = calculate_water(grams_protein)

#print("Protein (g):", grams_protein, "Water (g): ", grams_water)