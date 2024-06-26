# built-in dependencies
import math
import base64

# 3rd-party dependencies
import cv2
import numpy as np
import paho.mqtt.client as mqtt

# deepface
from deepface import DeepFace

# project dependencies
from promptface.utils.constants import DB_PATH, INFO_FORMAT, MODEL_NAME, BROKER_IP, BROKER_PORT, TOPIC_STREAM, DISCARD_PERCENTAGE
from promptface.utils.logger import Logger
from promptface.utils.abstract import AbstractOnVeried
from promptface.utils.folder_utils import createDirectory
from promptface.modules.pkl import load_pkl
from promptface.modules.streaming import AbstractPromptface

logger = Logger(__name__)


class Subscriber(AbstractPromptface):
    def __init__(self):
        super().__init__()
        self.broker_ip = BROKER_IP
        self.broker_port = BROKER_PORT
        self.topic_stream = TOPIC_STREAM
        self.img = np.zeros((160,160,3), np.uint8)
        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message


    def on_connect(self, client:mqtt.Client, userdata, flags, rc):
        logger.info("Connected with result code " + str(rc))
        client.subscribe(self.topic_stream)


    def on_message(self, client:mqtt.Client, userdata, msg):
        img = base64.b64decode(msg.payload)
        npimg = np.frombuffer(img, dtype=np.uint8)
        self.img = cv2.imdecode(npimg, 1)
        if self.threshold_size == 0:
            size = self.img.shape[0] * self.img.shape[1]
            self.threshold_size = int(math.sqrt(size*DISCARD_PERCENTAGE/100))
            logger.info('init threshold size: {}'.format(self.threshold_size))


    @classmethod
    def app(cls, callback:AbstractOnVeried, *args, **kwargs):
        # set app instance
        app_instance = cls()


        # ----- INIT -----
        try:
            # set logger
            createDirectory(DB_PATH)
            createDirectory('Logs')
            logger = Logger(__name__)
            logger.info(INFO_FORMAT.format('APP START'))

            # build model
            _ = DeepFace.build_model(model_name=MODEL_NAME)
            logger.info(f"{MODEL_NAME} is built")

            # load pickle
            # database_embeddings are vetorized from embeddings col
            database_embeddings, identities = load_pkl()

            # connect client
            app_instance.client.connect(app_instance.broker_ip, app_instance.broker_port)
            app_instance.client.loop_start()
        except Exception as e:
            logger.critical(str(e))
            exit(1)


        # ----- MAIN -----
        logger.info(INFO_FORMAT.format('START MAIN'))
        try:
            while True:
                # get img from new frame
                img = app_instance.img

                # get verified content and img processing like boxing face, etc...
                img = app_instance.process(img, database_embeddings, identities, False)

                # show
                # cv2.imshow("img", img)
                # Encoding the Frame
                _, buffer = cv2.imencode('.jpg', img)
                # Converting into encoded bytes
                jpg_as_text = base64.b64encode(buffer) # type: ignore
                app_instance.client.publish('web1', jpg_as_text)


                # enter only once when freeze
                # success
                if app_instance.target_distance and app_instance.target_path:
                    target_label = app_instance.target_path.split('/')[-1].split('\\')[-2]
                    logger.info(f"Hello, {target_label} {app_instance.target_distance} {app_instance.target_path}")
                    # --- do something like on/off green LEDs or save data, etc... ---
                    callback.on_verify_success(app_instance, *args, **kwargs)

                # failure
                if app_instance.target_distance and app_instance.target_path is None:
                    logger.info(f"Verify failed, {app_instance.target_distance}")
                    # --- do something like on/off red LEDs or save data, etc... ---
                    callback.on_verify_failed(app_instance, *args, **kwargs)

                app_instance.target_distance = None  # this means enter success and failure once per freeze


                # user input
                # https://stackoverflow.com/questions/35372700/whats-0xff-for-in-cv2-waitkey1
                key_code = cv2.waitKey(1) & 0xFF

                if key_code == ord("q"):
                    logger.info(INFO_FORMAT.format('QUIT'))
                    break
                if key_code == ord("r"):
                    logger.info(INFO_FORMAT.format('RE-LOAD IMG-DATABASE'))
                    database_embeddings, identities = load_pkl()
                    logger.info(INFO_FORMAT.format('RE-START MAIN'))

        except Exception as e:
            logger.critical(str(e))

        # ----- END -----
        # kill open cv things
        app_instance.client.loop_stop()
        app_instance.client.disconnect()
        cv2.destroyAllWindows()
        logger.info(INFO_FORMAT.format('END'))
