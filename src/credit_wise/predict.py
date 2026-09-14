from pathlib import Path
import pickle
import pandas as pd


# ============================================================
# LOAD MODEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "model"


with open(MODEL_DIR / "random_forest_model.pkl", "rb") as file:
    model = pickle.load(file)


with open(MODEL_DIR / "scaler.pkl", "rb") as file:
    scaler = pickle.load(file)


with open(MODEL_DIR / "one_hot_encoder.pkl", "rb") as file:
    ohe = pickle.load(file)


with open(MODEL_DIR / "education_encoder.pkl", "rb") as file:
    education_encoder = pickle.load(file)


with open(MODEL_DIR / "loan_encoder.pkl", "rb") as file:
    loan_encoder = pickle.load(file)


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_loan(input_data):

    input_df = pd.DataFrame([input_data])


    # ========================================================
    # LABEL ENCODING
    # ========================================================

    input_df["Education_Level"] = education_encoder.transform(
        input_df["Education_Level"]
    )


    # ========================================================
    # ONE-HOT ENCODING
    # ========================================================

    cols = [
        "Employment_Status",
        "Marital_Status",
        "Loan_Purpose",
        "Property_Area",
        "Gender",
        "Employer_Category",
    ]


    encoded = ohe.transform(input_df[cols])


    encoded_df = pd.DataFrame(
        encoded,
        columns=ohe.get_feature_names_out(cols),
        index=input_df.index,
    )


    # ========================================================
    # COMBINE ONE-HOT ENCODED COLUMNS
    # ========================================================

    input_df = pd.concat(
        [
            input_df.drop(columns=cols),
            encoded_df
        ],
        axis=1,
    )


    # ========================================================
    # REMOVE APPLICANT ID
    # ========================================================

    input_df = input_df.drop(
        "Applicant_ID",
        axis=1
    )


    # ========================================================
    # FEATURE ENGINEERING
    # ========================================================

    input_df["DTI_Ratio_sq"] = (
        input_df["DTI_Ratio"] ** 2
    )


    input_df["Credit_Score_sq"] = (
        input_df["Credit_Score"] ** 2
    )


    # ========================================================
    # REMOVE UNUSED FEATURES
    # ========================================================

    input_df = input_df.drop(
        columns=[
            "Credit_Score",
            "DTI_Ratio"
        ]
    )


    # ========================================================
    # MATCH TRAINING FEATURE ORDER
    # ========================================================

    input_df = input_df[
        scaler.feature_names_in_
    ]


    # ========================================================
    # FEATURE SCALING
    # ========================================================

    input_scaled = scaler.transform(
        input_df
    )


    # ========================================================
    # MAKE PREDICTION
    # ========================================================

    prediction = model.predict(
        input_scaled
    )


    # ========================================================
    # CONVERT PREDICTION TO ORIGINAL LABEL
    # ========================================================

    prediction_label = loan_encoder.inverse_transform(
        prediction
    )


    return prediction_label[0]