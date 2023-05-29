import os

defaultpath = os.path.join(os.getcwd(), "MachineLearnTest")

CUSTOM_MODEL_NAME = 'my_ssd_mobnet' 
PRETRAINED_MODEL_NAME = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
PRETRAINED_MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz'
TF_RECORD_SCRIPT_NAME = 'generate_tfrecord.py'
LABEL_MAP_NAME = 'label_map.pbtxt'



paths = {
    'WORKSPACE_PATH': os.path.join(defaultpath, 'Tensorflow', 'workspace'),
    'SCRIPTS_PATH': os.path.join(defaultpath, 'Tensorflow','scripts'),
    'APIMODEL_PATH': os.path.join(defaultpath, 'Tensorflow','models'),
    'ANNOTATION_PATH': os.path.join(defaultpath, 'Tensorflow', 'workspace','annotations'),
    'IMAGE_PATH': os.path.join(defaultpath, 'Tensorflow', 'workspace','images'),
    'MODEL_PATH': os.path.join(defaultpath, 'Tensorflow', 'workspace','models'),
    'PRETRAINED_MODEL_PATH': os.path.join(defaultpath, 'Tensorflow', 'workspace','pre-trained-models'),
    'CHECKPOINT_PATH': os.path.join(defaultpath, 'Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME), 
    'OUTPUT_PATH': os.path.join(defaultpath, 'Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'export'), 
    'TFJS_PATH':os.path.join(defaultpath, 'Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfjsexport'), 
    'TFLITE_PATH':os.path.join(defaultpath, 'Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfliteexport'), 
    'PROTOC_PATH':os.path.join(defaultpath, 'Tensorflow','protoc')
 }


print(f'os path join is {os.path.join(defaultpath,"tensorflow","workplace")}')

files = {
    'PIPELINE_CONFIG':os.path.join('Tensorflow', 'workspace','models', CUSTOM_MODEL_NAME, 'pipeline.config'),
    'TF_RECORD_SCRIPT': os.path.join(paths['SCRIPTS_PATH'], TF_RECORD_SCRIPT_NAME), 
    'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
}

for path in paths.values():
    if not os.path.exists(path):
        os.makedirs(path)
        print('creating {}'.format(path))



print('file creation process done')


VERIFICATION_SCRIPT = os.path.join(paths['APIMODEL_PATH'], 'research', 'object_detection', 'builders', 'model_builder_tf2_test.py')

print(f'verification script is {VERIFICATION_SCRIPT}')