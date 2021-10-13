import os
import tensorflow as tf

if __name__ == "__main__":
    print(f"Inside Python JOB ID = '{os.environ['SLURM_ARRAY_JOB_ID']}'")
    print(f"Inside Python TASK ID = '{os.environ['SLURM_ARRAY_TASK_ID']}")
    print("List GPU with Tensorflow: ", tf)
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        print("Name:", gpu.name, "  Type:", gpu.device_type)
