# CreditWise

AI-Powered Loan Approval Prediction System

CreditWise is a machine learning based web application that predicts whether a loan application is likely to be approved or rejected based on applicant information such as income, employment status, credit history, existing loans, loan amount, education, and other financial details.

The project uses a Random Forest Classifier trained on a loan approval dataset and provides predictions through a Flask web application.

---

## Live Demo

https://credit-wise-3dhz.onrender.com

> **Note:** Since CreditWise is hosted on Render's free tier, the application may take a little longer to load the first time after a period of inactivity.

---

## Features

- AI-based loan approval prediction
- Multi-step loan application form
- Applicant personal information collection
- Employment and financial information collection
- Loan details collection
- Machine learning based prediction
- Random Forest classification model
- Data preprocessing and feature engineering
- One-Hot Encoding for categorical features
- Label Encoding for education and loan approval
- StandardScaler for feature scaling
- Result checking/loading animation
- Responsive web interface
- Deployed online using Render

---

## Machine Learning Model

The project uses a:

**Random Forest Classifier**

The Random Forest model was selected after comparing multiple machine learning algorithms.

### Models Evaluated

- Logistic Regression
- K-Nearest Neighbors (KNN)
- Gaussian Naive Bayes
- Random Forest
- Gradient Boosting
- Extra Trees

Random Forest provided strong overall performance and was selected as the final model for the web application.

---

## Model Performance

The final Random Forest model achieved the following results on the test dataset:

| Metric | Score |
|---|---:|
| Accuracy | 91.00% |
| Precision | 84.13% |
| Recall | 86.89% |
| F1 Score | 85.48% |

### Confusion Matrix

```text
[[129  10]
 [  8  53]]
