import os
import requests
import datetime as dt

# NUTRITIONIX
NUTRI_APP_ID = "_GET_APP_ID_FROM_NUTRITIONIX_"
NUTRI_API_KEY = "_GET_API_KEY_FROM_NUTRITIONIX_"
REMOTE_USER = "0"  # set for testing account
EXERCISE_ENDPOINT = "_GET_ENDPOINT_FROM_NUTRITIONIX_"

# SHEETY
SHEETY_END = "_GET_ENDPOINT_FROM_SHEETY_"

# Date and time formatting
date = dt.datetime.now()
today = date.strftime("%x")
current_time = str(dt.datetime.now().time().replace(microsecond=0))

# testing params input set up for US standard units
gender = "_X_"  # Your input goes here
lbs = "_X_"  # Your input goes here
feet = "_X_"  # Your input goes here
inches = "_X_"  # Your input goes here
age = "_X_"  # Your input goes here

# conversion from US standard to metric units
weight = lbs / 2.205
height = ((feet * 12) + inches) * 2.54

# natural language input
did_what = input("What did you do today?").lower()

# NUTRITION PARAMS
nutrition_params = {
    "query": f"{did_what}",
    "gender": f"{gender}",
    "weight_kg": f"{weight}",
    "height_cm": f"{height}",
    "age": f"{age}",
}

# NUTRITION HEADER
nutrition_header = {
    "x-app-id": NUTRI_APP_ID,
    "x-app-key": NUTRI_API_KEY,
    "x-remote-user-id": REMOTE_USER,
}

# Nutritionix API post
nutrition_response = requests.post(url=EXERCISE_ENDPOINT, json=nutrition_params, headers=nutrition_header)
nutrition_response.raise_for_status()

# Sorted data to get to the calories burned
exercise_data = nutrition_response.json()["exercises"]
calories_burned = exercise_data[0]["nf_calories"]
duration = str(exercise_data[0]["duration_min"])
exercise = exercise_data[0]["user_input"]

# Sheety Json
sheety_input = {
    "workout": {
        "date": today,
        "time": current_time,
        "exercise": exercise,
        "duration": duration,
        "calories": calories_burned,
    }
}

# Sheety Header
sheety_headers = {
    "Authorization": "_GET_BASIC_AUTH_FROM_SHEETY_",
}

# Sheety API post
sheety_response = requests.post(SHEETY_END, json=sheety_input, headers=sheety_headers)
print(sheety_response.text)

