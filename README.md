# Car Seat Finder

A Streamlit web app that helps users narrow down car-seat options using:

- Child age, weight, and height
- Restraint stage
- Budget
- Narrow-seat / possible 3-across needs
- Front-to-back vehicle space
- Travel needs
- Rotation preference
- Material preference
- Infant-carrier preference

The app first filters out seats that do not fit the entered child in the selected
mode, then ranks the remaining seats using growth room, installation/ease-of-use
features, vehicle-fit considerations, practical features, and value.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install Streamlit:

```bash
pip install -r requirements.txt
```

4. Start the app:

```bash
streamlit run streamlit_app.py
```

A browser window should open automatically.

## Deploy free with Streamlit Community Cloud

1. Create a free GitHub account if you do not already have one.
2. Create a new GitHub repository.
3. Upload these files to the repository:
   - `streamlit_app.py`
   - `car_seat_finder.py`
   - `requirements.txt`
   - `README.md`
4. Sign in to Streamlit Community Cloud with GitHub.
5. Choose **Create app** / **Deploy an app**.
6. Select the GitHub repository.
7. Set the main file path to:

```text
streamlit_app.py
```

8. Deploy.

## Important

This is a shopping/research aid, not a substitute for the manufacturer manual,
vehicle manual, recall check, state law, or a Child Passenger Safety Technician.

The match score is not a crash-test safety score.

The starter catalog should be expanded and maintained before presenting the app
as a comprehensive consumer database.
