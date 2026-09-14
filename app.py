from flask import Flask, render_template, request, session, redirect


from src.credit_wise.predict import predict_loan


app = Flask(__name__)

app.config["SECRET_KEY"] = "creditwise-secret-key"


# ============================================================
# PERSONAL INFORMATION
# ============================================================

@app.route("/", methods=["GET", "POST"])
@app.route("/personal", methods=["GET", "POST"])
def personal():

    if request.method == "POST":

        session["personal"] = {
            "Age": int(request.form["Age"]),
            "Gender": request.form["Gender"],
            "Marital_Status": request.form["Marital_Status"],
            "Dependents": int(request.form["Dependents"]),
            "Education_Level": request.form["Education_Level"],
        }

        return redirect("/employment")


    return render_template(
        "personal.html",
        personal=session.get("personal", {})
    )


# ============================================================
# EMPLOYMENT INFORMATION
# ============================================================

@app.route("/employment", methods=["GET", "POST"])
def employment():

    # Make sure Personal Information was completed

    if "personal" not in session:

        return redirect("/personal")


    if request.method == "POST":

        session["employment"] = {
            "Employment_Status": request.form["Employment_Status"],
            "Employer_Category": request.form["Employer_Category"],
        }

        return redirect("/financial")


    return render_template(
        "employment.html",
        employment=session.get("employment", {})
    )


# ============================================================
# FINANCIAL INFORMATION
# ============================================================

@app.route("/financial", methods=["GET", "POST"])
def financial():

    # Make sure Employment Information was completed

    if "employment" not in session:

        return redirect("/employment")


    if request.method == "POST":

        session["financial"] = {
            "Applicant_Income": float(request.form["Applicant_Income"]),
            "Coapplicant_Income": float(request.form["Coapplicant_Income"]),
            "Savings": float(request.form["Savings"]),
            "Existing_Loans": int(request.form["Existing_Loans"]),
            "Credit_Score": float(request.form["Credit_Score"]),
            "DTI_Ratio": float(request.form["DTI_Ratio"]),
        }

        return redirect("/loan")


    return render_template(
        "financial.html",
        financial=session.get("financial", {})
    )


# ============================================================
# LOAN INFORMATION
# ============================================================

@app.route("/loan", methods=["GET", "POST"])
def loan():

    # Make sure Financial Information was completed

    if "financial" not in session:

        return redirect("/financial")


    if request.method == "POST":

        session["loan"] = {
            "Loan_Amount": float(request.form["Loan_Amount"]),
            "Loan_Term": int(request.form["Loan_Term"]),
            "Loan_Purpose": request.form["Loan_Purpose"],
            "Property_Area": request.form["Property_Area"],
            "Collateral_Value": float(request.form["Collateral_Value"]),
        }

        return redirect("/predict")


    return render_template(
        "loan.html",
        loan=session.get("loan", {})
    )


# ============================================================
# PREDICTION
# ============================================================

@app.route("/predict", methods=["GET"])
def predict():

    # Make sure all previous information exists

    if "personal" not in session:

        return redirect("/personal")


    if "employment" not in session:

        return redirect("/employment")


    if "financial" not in session:

        return redirect("/financial")


    if "loan" not in session:

        return redirect("/loan")


    # Combine all information

    input_data = {}

    input_data.update(session["personal"])
    input_data.update(session["employment"])
    input_data.update(session["financial"])
    input_data.update(session["loan"])


    # Add Applicant ID

    input_data["Applicant_ID"] = "WEB001"


    # Make Prediction

    prediction = predict_loan(input_data)


    # Prediction Message

    if prediction == "Yes":

        message = (
            "Based on the provided information, "
            "the model predicts that the loan may be approved."
        )

    else:

        message = (
            "Based on the provided information, "
            "the model predicts that the loan may not be approved."
        )


    # Clear Session

    session.clear()


    return render_template(
        "result.html",
        prediction=prediction,
        message=message
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)