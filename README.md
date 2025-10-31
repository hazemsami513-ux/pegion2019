
# Pigeon Breeding App (Streamlit)

This is a small Streamlit app that calculates breeding compatibility between male and female pigeons
based on target traits and trait weights. The compatibility formula is:

Compatibility = 100 - Σ(|trait_male - trait_female| × weight_of_trait)

## Files
- `streamlit_app.py` - main Streamlit app
- `data.csv` - sample dataset (id,gender,color,weight,head,feather,power,health,image_path)
- `images/` - sample placeholder images for pigeons
- `requirements.txt` - Python dependencies

## How to run locally
1. Create a Python virtual environment and activate it.
2. Install requirements: `pip install -r requirements.txt`
3. Run the app: `streamlit run streamlit_app.py`
4. Open the local URL shown in the terminal (usually http://localhost:8501).

## Deploy to Streamlit Cloud
1. Create a private GitHub repository (e.g., `pigeon-breeding-app`) and push the project files.
2. On Streamlit Cloud, click **New app**, select your GitHub repo and branch `main`, then `streamlit_app.py` as the main file.
3. Deploy — the app will be available privately in your Streamlit account.
