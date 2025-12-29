from flask import Blueprint, render_template
import pickle
import numpy as np

performance_bp = Blueprint('performance', __name__)

@performance_bp.route('/performance')
def index():
    # --- LOGIKA UNTUK DECISION TREE ---
    try:
        with open('models/model_sentimen_decision_tree.pkl', 'rb') as f:
            pipeline_dt = pickle.load(f)
        
        tfidf = pipeline_dt.named_steps['tfidf']
        model_dt = pipeline_dt.named_steps['classifier']
        feature_names = tfidf.get_feature_names_out()
        importances = model_dt.feature_importances_
        
        top_indices = np.argsort(importances)[-5:][::-1]
        top_words_dt = [{"word": feature_names[i], "score": round(importances[i], 4)} for i in top_indices]
    except:
        top_words_dt = []

    # --- DATA STATISTIK DARI NOTEBOOK (Untitled7.ipynb) ---
    metrics = {
        'total_data': 475, # Total data unik setelah drop_duplicates
        'knn': {
            'accuracy': 0.93, # Akurasi Test Set KNN
            'cv_avg': 0.85,    # Rata-rata Cross-Val KNN
            'matrix': {'tn': 43, 'fp': 7, 'fn': 0, 'tp': 45}, # Hasil Confusion Matrix KNN
            'top_words': ['cepat', 'sering', 'buruk', 'kurang', 'nyaman'], # Chi-Square Proxy
            'report': {
                'negatif': {'precision': 1.00, 'recall': 0.86, 'f1': 0.92},
                'positif': {'precision': 0.87, 'recall': 1.00, 'f1': 0.93}
            }
        },
        'dt': {
            'accuracy': 0.87, 
            'cv_avg': 0.77,
            'matrix': {'tn': 40, 'fp': 10, 'fn': 2, 'tp': 43},
            'report': {
                'negatif': {'precision': 0.95, 'recall': 0.80, 'f1': 0.87},
                'positif': {'precision': 0.81, 'recall': 0.96, 'f1': 0.88}
            }
        }
    }

    return render_template('performance/index.html', 
                           metrics=metrics, 
                           top_words_dt=top_words_dt)