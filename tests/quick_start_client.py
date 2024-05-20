# project dependencies
from promptface.MQTTPromptface import Publisher
from promptface.utils.constants import RASPI_IP, RASPI_PORT, RASPI_TOPIC

# Main
publisher = Publisher(RASPI_IP, RASPI_PORT, RASPI_TOPIC)
publisher.client()