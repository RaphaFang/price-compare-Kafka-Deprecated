import asyncio
from confluent_kafka import Consumer, KafkaError, KafkaException
import json
from config import consumer_conf
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

consumer = Consumer(consumer_conf)
consumer.subscribe(['ebay_topic'])

async def start_ebay_consumer():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                logging.debug("No message received. Polling again.")
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # 正常讀完區塊資料的回報
                    logging.info(f"End of partition reached {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                    continue
                else:
                    logging.error(f"Error occurred: {msg.error()}")
                    break

            data = json.loads(msg.value().decode('utf-8'))
            logging.debug(f"consumer_ebay 23 {data}")
            print("consumer_ebay 23", data, flush=True)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
