import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util

CUSTOM_MODEL_NAME = 'my_ssd_mobnet' 
PRETRAINED_MODEL_NAME = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
PRETRAINED_MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz'
TF_RECORD_SCRIPT_NAME = 'generate_tfrecord.py'
LABEL_MAP_NAME = 'label_map.pbtxt'

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

mainpath = os.path.join(os.getcwd(), "test123")

paths = {
    'WORKSPACE_PATH': os.path.join(mainpath, 'Tensorflow', 'workspace'),
    'SCRIPTS_PATH': os.path.join(mainpath, 'Tensorflow','scripts'),
    'APIMODEL_PATH': os.path.join(mainpath, 'Tensorflow','models'),
    'ANNOTATION_PATH': os.path.join(mainpath, 'Tensorflow', 'workspace','annotations'),
    'IMAGE_PATH': os.path.join(mainpath, 'Tensorflow', 'workspace','images'),
    'MODEL_PATH': os.path.join(mainpath, 'Tensorflow', 'workspace','models'),
    'PRETRAINED_MODEL_PATH': os.path.join(mainpath, 'Tensorflow', 'workspace','pre-trained-models'),
    'CHECKPOINT_PATH': os.path.join(mainpath, 'Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME), 
    'OUTPUT_PATH': os.path.join(mainpath, 'Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'export'), 
    'TFJS_PATH':os.path.join(mainpath, 'Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfjsexport'), 
    'TFLITE_PATH':os.path.join(mainpath, 'Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfliteexport'), 
    'PROTOC_PATH':os.path.join(mainpath, 'Tensorflow','protoc')
 }

files = {
    'PIPELINE_CONFIG':os.path.join(mainpath, 'Tensorflow', 'workspace','models', CUSTOM_MODEL_NAME, 'pipeline.config'),
    'TF_RECORD_SCRIPT': os.path.join(paths['SCRIPTS_PATH'], TF_RECORD_SCRIPT_NAME), 
    'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
}


for path in paths.values():
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'path created {path}')
        

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)

print(f"ckpt is {ckpt}")

print(f"path is {os.path.join(paths['CHECKPOINT_PATH'], 'ckpt-0')}")

ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'],'checkpoint', 'ckpt-0')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

print('importing for machine learn testing and evaluation.')
import cv2 
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
print('importing complete')

os.environ['MPLBACKEND'] = 'Qt5Agg'

plt.ion()
print('plt activated')



category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])


IMAGE_PATH = os.path.join(paths['IMAGE_PATH'], 'test', 'one.baefe8fb-fa67-11ed-8682-dc41a9eed7f1.jpg')
print('imgpath done')
img = cv2.imread(IMAGE_PATH)
image_np = np.array(img)

input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
detections = detect_fn(input_tensor)
print('tensor detection complete')

num_detections = int(detections.pop('num_detections'))
detections = {key: value[0, :num_detections].numpy()
              for key, value in detections.items()}
detections['num_detections'] = num_detections

# detection_classes should be ints.
detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

label_id_offset = 1
print('label_id_offset = 1 set')
image_np_with_detections = image_np.copy()

viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes']+label_id_offset,
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=.8,
            agnostic_mode=False)

plt.imshow(cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB))

plt.show(block = True)

# plt.write(__name__ = "test.png")

print('writing process done')
