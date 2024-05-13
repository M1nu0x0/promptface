# promptface
custom deepface(v0.0.91) fork repo

## Installation
Recommend install promptface and deepface(0.0.91) is to download it from github. It's going to install the library itself and its prerequisites as well.
```console
$ pip install git+https://github.com/M1nu0x0/promptface.git
```

Also, you can install promptface from its source code.
```
$ git clone https://github.com/M1nu0x0/promptface.git
$ cd promptface
$ pip install -e .
```

Then you will be able to import the library and use its functionallities.
```python
from deepface import Deepface   # However the version of deepface is 0.0.91
from promptface.modules.app import app
```

## How to use

### deepface
You can read README.md from [deepface](https://github.com/serengil/deepface) repository.

### promptface
You can use the promptface by running quick_start.py and write constants.json.

There is examples of quick_start.py and constants.json
```py
# recommend python 3.8.12 version
# project dependencies
from promptface.Promptface import app


# --- do something like on/off green LEDs or save data, etc... ---
def on_verify_success(x, y):
    print('x + y = {}'.format(x+y))
    print(app.target_path, app.target_distance)


# --- do something like on/off red LEDs or save data, etc... ---
def on_verify_failure():
    print(app.target_path, app.target_distance)


# How to Use app
app(on_verify_success, on_verify_failure, params1=(1, 3), params2=())

# pass None when you don't want to pass the function in app()
# app(None, None)
```
```json
{
    "DB_PATH": "./ImgDataBase",
    "MODEL_NAME": null,
    "DETECTOR_BACKEND": null,
    "ENFORCE_DETECTION": true,
    "ALIGN": true,
    "SOURCE": 0,
    "TIME_THRESHOLD": 5,
    "FRAME_THRESHOLD": 10
}
```

There is an example of a database folder format that was modified a little from Deepface Streaming.

```
root
├──main.py
├──constants.json
├──Logs
│   ├── promptface.log
├── ImgDataBase
│   ├── Alice
│   │   ├── Alice01.jpg
│   │   ├── Alice02.jpg
│   ├── Bob
│   │   ├── Bob01.jpg
```

Some logic has been changed in comparison to deepface
- The cosine_distance measurement method has been changed to use scikit-learn.
- Sort df in identity order.
- You can do something when verifies

## License

PromptFace is licensed under the MIT License - see [`LICENSE`](https://github.com/M1nu0x0/prompt_face/blob/master/LICENSE) for more details.

## About DeepFace License
DeepFace wraps some external face recognition models: [VGG-Face](http://www.robots.ox.ac.uk/~vgg/software/vgg_face/), [Facenet](https://github.com/davidsandberg/facenet/blob/master/LICENSE.md), [OpenFace](https://github.com/iwantooxxoox/Keras-OpenFace/blob/master/LICENSE), [DeepFace](https://github.com/swghosh/DeepFace), [DeepID](https://github.com/Ruoyiran/DeepID/blob/master/LICENSE.md), [ArcFace](https://github.com/leondgarse/Keras_insightface/blob/master/LICENSE), [Dlib](https://github.com/davisking/dlib/blob/master/dlib/LICENSE.txt), [SFace](https://github.com/opencv/opencv_zoo/blob/master/models/face_recognition_sface/LICENSE) and [GhostFaceNet](https://github.com/HamadYA/GhostFaceNets/blob/main/LICENSE). Besides, age, gender and race / ethnicity models were trained on the backbone of VGG-Face with transfer learning. Similarly, DeepFace wraps many face detectors: [OpenCv](https://github.com/opencv/opencv/blob/4.x/LICENSE), [Ssd](https://github.com/opencv/opencv/blob/master/LICENSE), [Dlib](https://github.com/davisking/dlib/blob/master/LICENSE.txt), [MtCnn](https://github.com/ipazc/mtcnn/blob/master/LICENSE), [Fast MtCnn](https://github.com/timesler/facenet-pytorch/blob/master/LICENSE.md), [RetinaFace](https://github.com/serengil/retinaface/blob/master/LICENSE), [MediaPipe](https://github.com/google/mediapipe/blob/master/LICENSE), [YuNet](https://github.com/ShiqiYu/libfacedetection/blob/master/LICENSE), [Yolo](https://github.com/derronqi/yolov8-face/blob/main/LICENSE) and [CenterFace](https://github.com/Star-Clouds/CenterFace/blob/master/LICENSE). License types will be inherited when you intend to utilize those models. Please check the license types of those models for production purposes.


DeepFace [logo](https://thenounproject.com/term/face-recognition/2965879/) is created by [Adrien Coquet](https://thenounproject.com/coquet_adrien/) and it is licensed under [Creative Commons: By Attribution 3.0 License](https://creativecommons.org/licenses/by/3.0/).
