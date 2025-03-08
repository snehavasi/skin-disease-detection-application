# from flask import Flask, request, render_template
# import tensorflow as tf
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.image import img_to_array
# from PIL import Image
# import numpy as np
# import os
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


# app = Flask(__name__)
# model = load_model("skin_disease_model.h5")


# #Defining the classes

# # class_names  =["Cellulitis", "Impetigo", "Athelete-Foot", "Nail-Fungus", "Ringworm","Cutaneous-larva-migrans","Chickenpox", "Shingles"]
# class_names = ["Actinic", "Acne", "Melanoma"]

# #Preparing the image before feeding it to the model
# def preprocess_image(img, target_size):
#     img = img.resize(target_size)
#     im = img_to_array(img)
#     img = np.expand_dims(img, axis =0)
#     img = img / 255.0
#     return img


# #Defining the routes
# @app.route("/", methods =["GET", "POST"])
# def predict():
#     if request.method == "POST":
#         file = request.files["file"]

#         if file:
#             image = Image.open(file.stream)
#             image = preprocess_image(image, target_size=(150,150))
#             prediction = model.predict(image)
#             predicted_class = class_names[np.argmax(prediction)]

#             return render_template("index.html", prediction =  predicted_class)
        
#     return render_template("index.html")
    

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, render_template
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import os

# Disable TensorFlow OneDNN optimizations for debugging
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__)

# Load model with error handling
try:
    model = load_model("skin_disease_model.h5")
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {str(e)}")
    model = None

# Define class labels (Ensure they match the model's training classes)
class_names = ["Actinic", "Acne", "Melanoma"]

# Function to preprocess the image
def preprocess_image(img, target_size=(256, 256)):
    try:
        img = img.resize(target_size)  # Resize to match model input size
        img = img.convert("RGB")  # Convert to RGB to avoid grayscale issues
        img = img_to_array(img)  # Convert image to array
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        img = img.astype("float32") / 255.0  # Normalize
        return img
    except Exception as e:
        print(f"❌ Error in image preprocessing: {str(e)}")
        return None

# Route for file upload and prediction
@app.route("/", methods=["GET", "POST"])
def predict():
    prediction = None
    prediction_class = None
    confidence = None
    error_message = None

    if request.method == "POST":
        file = request.files.get("file")

        if file:
            try:
                print("📤 File received")
                image = Image.open(file.stream)
                processed_image = preprocess_image(image)

                if processed_image is None:
                    error_message = "Error in image preprocessing."
                else:
                    print(f"🔍 Processed Image Shape: {processed_image.shape}")

                    # Validate model before prediction
                    if model is not None:
                        try:
                            prediction = model.predict(processed_image)
                            predicted_class = class_names[np.argmax(prediction)]
                            confidence = np.max(prediction) * 100  # Confidence score
                            print(f"✅ Prediction: {predicted_class} ({confidence:.2f}%)")
                            return render_template("index.html", prediction_name =  predicted_class, confidence=f"{confidence:.2f}%" if confidence else None)
                        except Exception as e:
                            error_message = f"Prediction error: {str(e)}"
                    else:
                        error_message = "Model is not loaded correctly."

            except Exception as e:
                error_message = f"Error processing image: {str(e)}"

    return render_template(
        "index.html",
        error=error_message
    )

if __name__ == "__main__":
    app.run(debug=True)