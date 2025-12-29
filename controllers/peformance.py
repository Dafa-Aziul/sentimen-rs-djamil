import os
import pickle
import numpy as np
from flask import Blueprint, render_template

performance_bp = Blueprint('performance', __name__)

# Gunakan Path Absolut agar PythonAnywhere tidak error
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DT_PATH = os.path.join(BASE_DIR, 'models', 'model_sentimen_decision_tree.pkl')

@performance_bp.route('/performance')
def index():
    # --- 1. AMBIL DATA DINAMIS DARI MODEL DECISION TREE ---
    top_words_dt = []
    try:
        with open(MODEL_DT_PATH, 'rb') as f:
            pipeline_dt = pickle.load(f)
        
        tfidf = pipeline_dt.named_steps['tfidf']
        model_dt = pipeline_dt.named_steps['classifier']
        feature_names = tfidf.get_feature_names_out()
        importances = model_dt.feature_importances_
        
        # Ambil 5 kata dengan pengaruh (Gini Importance) tertinggi
        top_indices = np.argsort(importances)[-5:][::-1]
        top_words_dt = [
            {"word": feature_names[i], "score": round(importances[i], 4)} 
            for i in top_indices if importances[i] > 0
        ]
    except Exception as e:
        print(f"Gagal memuat Top Words DT: {e}")
        # Data cadangan jika file pkl tidak terbaca
        top_words_dt = [{"word": "tidak_termuat", "score": 0}]

    # --- 2. SETUP METRICS (Masukkan top_words ke dalam dictionary) ---
    metrics = {
        'total_data': 475,
        'knn': {
            'accuracy': 0.93,
            'cv_avg': 0.85,
            'matrix': {'tn': 43, 'fp': 7, 'fn': 0, 'tp': 45},
            # Menambahkan skor Chi-Square (Hasil dari Notebook Anda)
            'top_words': [
                {'word': 'cepat', 'score': 18.4201},
                {'word': 'sering', 'score': 12.1532},
                {'word': 'buruk', 'score': 10.8845},
                {'word': 'kurang', 'score': 9.5412},
                {'word': 'nyaman', 'score': 8.2109}
            ],
            'report': {
                'negatif': {'precision': 1.00, 'recall': 0.86, 'f1': 0.92},
                'positif': {'precision': 0.87, 'recall': 1.00, 'f1': 0.93}
            }
        },
        'dt': {
            'accuracy': 0.87, 
            'cv_avg': 0.77,
            'matrix': {'tn': 40, 'fp': 10, 'fn': 2, 'tp': 43},
            # SEKARANG DATA DT MASUK KE SINI
            'top_words': top_words_dt, 
            'report': {
                'negatif': {'precision': 0.95, 'recall': 0.80, 'f1': 0.87},
                'positif': {'precision': 0.81, 'recall': 0.96, 'f1': 0.88}
            }
        }
    }

    return render_template('performance/index.html', metrics=metrics)