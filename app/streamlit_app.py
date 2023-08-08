import pandas as pd
import numpy as np

import requests
import pickle
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from streamlit_lottie import st_lottie_spinner


# Load the model
loaded_model = pickle.load(open("../Model/RF_Regressor.pkl", "rb"))


def main():
    # Emoji Constants
    EMOJI_MONEY_BAG = "💰"

    st.write(
        """
    # Approved loan amount prediction
    This app predicts how much will be granted to a loan applicant. Just fill in the following information and click on the Predict button.
    """
    )

    # Gender input
    st.write(
        """
    ## Gender
    """
    )
    input_gender = st.radio("Select you gender", ["Male", "Female"], index=0)

    # Age input slider
    st.write(
        """
    ## Age
    """
    )
    input_age = st.slider(
        "Select your age", value=40, min_value=18, max_value=65, step=1
    )

    # Income
    st.write(
        """
    ## Income
    """
    )
    input_income = st.slider(
        "Select your income (biweekly)",
        value=2500,
        min_value=0,
        max_value=7000,
        step=10,
    )

    # Income stability
    st.write(
        """
    ## Income stability
    """
    )
    income_stab = st.radio("How is your income stability", ["Low", "High"], index=0)

    # Profession dropdown
    st.write(
        """
    ## Profession
    """
    )
    professions = [
        "Working",
        "Commercial associate",
        "Pensioner",
        "State servant",
        "Other",
    ]
    input_professions = st.selectbox("Select your profession", professions)

    # Residence location dropdown
    st.write(
        """
    ## Residence location
    """
    )
    locations = ["Semi-Urban", "Rural", "Urban"]
    location = st.selectbox("Select your residence location", locations)

    # Current loan expenses
    st.write(
        """
    ## Current loan expenses
    """
    )
    input_current_loan_amt = st.slider(
        "Select your current loan expenses",
        value=0,
        min_value=0,
        max_value=1000,
        step=10,
    )

    # Expenses type 1
    st.write(
        """
    ## Expenses type 1
    """
    )
    exp_type_one = st.radio("Do you have expenses type one?", ["Yes", "No"], index=1)

    # Expenses type 2
    st.write(
        """
    ## Expenses type 2
    """
    )
    exp_type_two = st.radio("Do you have expenses type two?", ["Yes", "No"], index=1)

    # Number of dependents
    st.write(
        """
    ## Number of dependents
    """
    )
    dependents_count = st.slider(
        "How many dependents do you have?", value=0, min_value=0, max_value=4, step=1
    )

    # Credit score
    st.write(
        """
    ## Credit score
    """
    )
    credit_score = st.slider(
        "Select your credit score", value=740, min_value=580, max_value=900, step=1
    )

    # Loan default
    st.write(
        """
    ## Loan default
    """
    )
    loan_default_dict = {"Yes": 1, "No": 0}
    loan_default_input = st.radio(
        "Have you ever had a loan default", ["Yes", "No"], index=1
    )
    loan_default_input_val = loan_default_dict.get(loan_default_input)

    # Has a credit card
    st.write(
        """
    ## Credit card
    """
    )
    cc_status = ["Active", "Inactive", "Unpossessed"]
    cc_status_input = st.selectbox("What is the status of your credit card", cc_status)

    # Property price
    st.write(
        """
    ## Property price
    """
    )
    prop_price = st.slider(
        "Select your property price", value=0, min_value=0, max_value=400000, step=100
    )

    # Property type
    st.write(
        """
    ## Property type
    """
    )
    property_type = [1, 2, 3, 4]
    property_type_input = st.selectbox("Select the property type", property_type)

    # Property location dropdown
    st.write(
        """
    ## Property location
    """
    )
    prop_locations = ["Semi-Urban", "Rural", "Urban"]
    prop_location = st.selectbox("Select your property location", prop_locations)

    # Co-applicant
    st.write(
        """
    ## Co-applicant
    """
    )
    co_applicant_dict = {"Yes": 1, "No": 0}
    co_applicant = st.radio("Do you have a co-applicant?", ["Yes", "No"], index=1)
    co_applicant_val = co_applicant_dict.get(co_applicant)

    # Loan amount requested
    st.write(
        """
    ## Loan amount requested
    """
    )
    loan_amount_req = st.slider(
        "Select your current loan expenses",
        value=0,
        min_value=0,
        max_value=600000,
        step=100,
    )

    # Predict Button
    predict_bt = st.button("Predict " + EMOJI_MONEY_BAG)
    st.markdown("##")
    st.markdown("##")

    # Categorical mappings
    gender_mapping = {"Female": 0, "Male": 1}
    Profession_mapping = {
        "Commercial associate": 0,
        "Other": 1,
        "Pensioner": 2,
        "State servant": 3,
        "Working": 5,
    }
    Income_Stability_mapping = {"High": 0, "Low": 1}
    Expense_Type_1_mapping = {"No": 0, "Yes": 1}
    Expense_Type_2_mapping = {"No": 0, "Yes": 1}
    Location_mapping = {"Rural": 0, "Semi-Urban": 1, "Urban": 2}
    Has_Active_Credit_Card_mapping = {
        "Active": 0,
        "Inactive": 1,
        "Unknown": 2,
        "Unpossessed": 3,
    }
    Property_Location = {"Rural": 0, "Semi-Urban": 1, "Urban": 2}

    @st.cache_data(show_spinner=False)
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_loading_an = load_lottieurl(
        "https://assets3.lottiefiles.com/packages/lf20_szlepvdh.json"
    )

    # DataFrame creation triggered when the Predict button is clicked
    if predict_bt:
        # Mapping categorical inputs to numerical values
        input_gender_val = gender_mapping.get(input_gender)
        input_professions_val = Profession_mapping.get(input_professions)
        income_stab_val = Income_Stability_mapping.get(income_stab)
        exp_type_one_val = Expense_Type_1_mapping.get(exp_type_one)
        exp_type_two_val = Expense_Type_2_mapping.get(exp_type_two)
        location_val = Location_mapping.get(location)
        cc_status_input_val = Has_Active_Credit_Card_mapping.get(cc_status_input)
        prop_location_val = Property_Location.get(prop_location)

        # list of all the inputs
        profile_to_predict = {
            "Gender": input_gender_val,
            "Age": input_age,
            "Income (USD)": input_income,
            "Income Stability": income_stab_val,
            "Profession": input_professions_val,
            "Location": location_val,
            "Loan Amount Request (USD)": loan_amount_req,
            "Current Loan Expenses (USD)": input_current_loan_amt,
            "Expense Type 1": exp_type_one_val,
            "Expense Type 2": exp_type_two_val,
            "Dependents": dependents_count,
            "Credit Score": credit_score,
            "No. of Defaults": loan_default_input_val,
            "Has Active Credit Card": cc_status_input_val,
            "Property Type": property_type_input,
            "Property Location": prop_location_val,
            "Co-Applicant": co_applicant_val,
            "Property Price": prop_price,
        }

        profile_to_predict_df = pd.DataFrame(
            [profile_to_predict.values()], columns=profile_to_predict.keys()
        )
        # st.write(profile_to_predict_df)
        with st_lottie_spinner(
            lottie_loading_an, quality="high", height="200px", width="200px"
        ):
            final_pred = loaded_model.predict(profile_to_predict_df)
        # if final_pred exists, then stop displaying the loading animation
        st.info(
            f"## You have been granted a loan amount up to {round(final_pred[0],2)} USD"
        )
        st.balloons()


if __name__ == "__main__":
    main()
