import tensorflow as tf

def build_autoencoder(input_dim):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(input_dim,)),

        # Encoder
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(8, activation='relu'),

        # Bottleneck
        tf.keras.layers.Dense(4, activation='relu'),

        # Decoder
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),

        # Output
        tf.keras.layers.Dense(input_dim)
    ])

    model.compile(optimizer='adam', loss='mse')

    return model