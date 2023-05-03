import pyinotify
from datetime import datetime, tzinfo, timedelta
import argparse
import pika
import warnings
warnings.filterwarnings("ignore")


class Log(pyinotify.ProcessEvent):
    def my_init(self, fileobj, channel):
        self._fileobj = fileobj
        self._channel = channel

    def process_default(self, event):
        message = str(str(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")) + \
                      '\t' + str(event.maskname) + '\t' + str(event.name)+ \
                      '\t'  + str(event.pathname) + '\n')
        message_to_mq = str({"createdAt" : str(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")),
                         "eventName" : str(event.maskname),
                         "file" : str(event.name),
                         "fullPath": str(event.pathname)})
        self._channel.basic_publish(exchange='', routing_key='NasMonitor', body=message_to_mq)
        self._fileobj.write(message)
        self._fileobj.flush()


class TrackModifications(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        print('IN_MODIFY')

class Empty(pyinotify.ProcessEvent):
    def my_init(self, msg):
        self._msg = msg

    def process_default(self, event):
        print(self._msg)


def parse_cli_arguments():
    parser = argparse.ArgumentParser(
        u"Python PyiNotifier events watcher and logger"
    )
    parser.add_argument(u"--monitor_dir", required=True, type=str, help="Directory to watch, e.g. -> './testdir/' ")
    parser.add_argument(u"--logs_dir", required=False, type=str, default='./pyinotify_moonbug_NAS_log.log',
                        help="Directory to save logs, e.g. -> './logs/logs.log/' ")
    parser.add_argument(u"--usr", required=True, type=str, help="Username for RabbitMQ account")
    parser.add_argument(u"--pwd", required=True, type=str, help="Password for RabbitMQ account")
    parser.add_argument(u"--env", required=True, type=str, help="Environment for RabbitMQ service")
    return parser.parse_args()


def monitor():
    # pyinotify:
    parsed_cli_arguments = parse_cli_arguments()
    monitor_dir = parsed_cli_arguments.monitor_dir
    logs_dir = parsed_cli_arguments.logs_dir

    # RabbitMQ Credentials
    rabbit_host = "35.234.130.164"
    rabbit_port = 5672
    rabbit_username = parsed_cli_arguments.usr
    rabbit_password = parsed_cli_arguments.pwd
    rabbit_env = parsed_cli_arguments.env

    logs_outputs = open(logs_dir, "a")

    rabbit_params = pika.ConnectionParameters(host=rabbit_host, port=rabbit_port, virtual_host= rabbit_env,
                                              credentials=pika.PlainCredentials(username=rabbit_username,
                                                                                password=rabbit_password))
    rabbit_connection = pika.BlockingConnection(rabbit_params)

    try:
        # Rabbit MQ messaging
        rabbit_channel = rabbit_connection.channel()
        rabbit_channel.queue_declare(queue='NasMonitor', durable=True)

        # Messaging Notifier
        watch_manager = pyinotify.WatchManager()
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_DELETE_SELF | pyinotify.IN_MOVE_SELF | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO
        handler = Empty(TrackModifications(Log(fileobj=logs_outputs, channel=rabbit_channel)), msg = "Logs updated.")
        notifier = pyinotify.Notifier(watch_manager, default_proc_fun=handler)
        watch_manager.add_watch(monitor_dir, mask=mask, rec=True, auto_add=True)
        notifier.loop()
    except KeyboardInterrupt:
        logs_outputs.close()
        rabbit_connection.close()
    finally:
        logs_outputs.close()
        rabbit_connection.close()


if __name__ == "__main__":
    monitor()