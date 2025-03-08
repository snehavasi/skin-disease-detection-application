import tensorflow as tf

# Load the .keras model
model = tf.keras.models.load_model("skin_disease_model_2.keras")

# Save it as an .h5 file
model.save("skin_disease_model.h5")

print("Model converted successfully!")
