# To Bulk or Not To Bulk 🏋️⚖️

A complete fitness and nutrition calculator integrating **FastAPI** for backend computations and **Streamlit** for interactive visualization.

Based on exercise physiology principles and the **Eventual Weight Change (EWC)** dynamic weight change models (Mifflin-St Jeor BMR, Hall et al. energy balance).

---

## Features
- **BMI (Body Mass Index)** with classification (Underweight, Normal, Overweight, Obesity, Extreme Obesity).
- **BMR (Basal Metabolic Rate)** calculation via Mifflin-St Jeor equation.
- **TDEE (Total Daily Energy Expenditure)** with activity multipliers (Sedentary, Lightly Active, Moderately Active, Very Active, Extremely Active).
- **Goal Configuration**: Maintain, Bulking (Surplus), or Cutting (Deficit) with Recommended (10%), Aggressive (15%), Very Aggressive (20%), or custom percentage pacing.
- **Eventual Weight Change (EWC)**: 3-year projection and milestone projections (1 month, 3 months, 6 months, 1 year, 1.5 years).
- **Macronutrient Breakdown**: Protein, Fat, and Carb allocation tailored to bulking/cutting targets.
- **Dual Unit Support**: Metric (`kg`, `cm`) and Imperial (`lbs`, `inches`).

---

## How to Run

### 1. Run the FastAPI Backend
Start the FastAPI server on port 8000:
```bash
uv run uvicorn to_bulk_or_not_to_bulk.api:app --reload --port 8000
```
- Interactive Swagger API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI schema: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

### 2. Run the Streamlit Frontend
In a separate terminal, launch the Streamlit interface:
```bash
uv run streamlit run src/to_bulk_or_not_to_bulk/app.py
```
*(Streamlit connects to `http://127.0.0.1:8000` by default; custom backend URL can be configured via `API_URL` environment variable).*
