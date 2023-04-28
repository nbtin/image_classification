import tensorflow as tf

# Download the ResNet model from TensorFlow Hub
MODEL_URL = 'https://tfhub.dev/google/imagenet/resnet_v2_50/feature_vector/5'
model = tf.keras.Sequential([tf.keras.layers.InputLayer(input_shape=(224, 224, 3)),
                             tf.keras.applications.ResNet50V2(input_shape=(224, 224, 3),
                                                               include_top=True,
                                                               weights='imagenet')])
model.compile()
model.save('models/resnet.h5')
model.summary()
