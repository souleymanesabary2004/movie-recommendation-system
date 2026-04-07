# src/models/compress_models.py
# Compress ML models to reduce file size

import joblib
import os
import time

print("="*50)
print("MODEL COMPRESSION")
print("="*50)

models_dir = 'models/'
models = [
    'svd_model.pkl',
    'knn_model.pkl', 
    'content_model.pkl',
    'hybrid_model.pkl'
]

print(f"\n🔍 Searching for models in {models_dir}")

for model_name in models:
    original_path = os.path.join(models_dir, model_name)
    compressed_path = original_path.replace('.pkl', '_compressed.pkl')
    
    if os.path.exists(original_path):
        print(f"\n📦 Compressing {model_name}...")
        
        # Load original
        start = time.time()
        model = joblib.load(original_path)
        load_time = time.time() - start
        
        # Save with compression (level 3)
        start = time.time()
        joblib.dump(model, compressed_path, compress=3)
        compress_time = time.time() - start
        
        # Compare sizes
        original_size = os.path.getsize(original_path) / 1024 / 1024
        compressed_size = os.path.getsize(compressed_path) / 1024 / 1024
        reduction = (1 - compressed_size / original_size) * 100
        
        print(f"   Original: {original_size:.2f} MB")
        print(f"   Compressed: {compressed_size:.2f} MB")
        print(f"   Reduction: {reduction:.1f}%")
        print(f"   Load time: {load_time:.2f}s")
        print(f"   Compress time: {compress_time:.2f}s")
    else:
        print(f"\n⚠️  {model_name} not found - skipped")

print("\n" + "="*50)
print("✅ Model compression completed!")
print("   Compressed models saved with '_compressed.pkl'")
print("="*50)