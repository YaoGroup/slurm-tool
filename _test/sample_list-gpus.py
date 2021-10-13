import tensorflow as tf

if __name__ == "__main__":
    print("List GPU with Tensorflow: ", tf)
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        print("Name:", gpu.name, "  Type:", gpu.device_type)
