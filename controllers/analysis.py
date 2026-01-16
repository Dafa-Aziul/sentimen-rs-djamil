from flask import Blueprint, render_template, request
import pickle
from utils.preprocessor import clean_text

analysis_bp = Blueprint('analysis', __name__)

try:
    with open('models/model_sentimen_knn.pkl', 'rb') as f:
        model_knn = pickle.load(f)
    with open('models/model_sentimen_decision_tree.pkl', 'rb') as f:
        model_dt = pickle.load(f)
except Exception as e:
    print(f"Error memuat model: {e}")

@analysis_bp.route('/analysis')
def index():
    return render_template('analysis/index.html')

@analysis_bp.route('/predict', methods=['POST'])
def predict():
    komentar = request.form.get('komentar')
    if not komentar:
        return "<p class='text-red-500 font-bold'>Teks tidak boleh kosong!</p>"

    cleaned = clean_text(komentar)
    
    
    if not cleaned.strip():
        return "<p class='text-red-500 italic'>Maaf, teks tidak mengandung kata yang dikenali model.</p>"

    res_knn = model_knn.predict([cleaned])[0]
    res_dt = model_dt.predict([cleaned])[0]

    prob_knn = max(model_knn.predict_proba([cleaned])[0]) * 100
    prob_dt = max(model_dt.predict_proba([cleaned])[0]) * 100
    
    return render_template('analysis/result_partial.html', 
                           original=komentar, 
                           res_knn=res_knn, res_dt=res_dt,
                           conf_knn=f"{prob_knn:.2f}%", 
                           conf_dt=f"{prob_dt:.2f}%")