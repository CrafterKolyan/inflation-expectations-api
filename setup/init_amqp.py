#
# Created by Maksim Eremeev (mae9785@nyu.edu)
#

import argparse

from rmq_interface import RabbitMQInterface


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-dq', '--api_queue', nargs='*', help='queue name for the inference worker')
    parser.add_argument('-c', '--connect', nargs='*', help='amqp connect string')
    args = parser.parse_args()

    interface = RabbitMQInterface(url_parameters=args.connect[0])

    interface.create_queue(name=args.api_queue[0],
                           exchnage_to_bind='amq.topic',
                           binding_routing_key=args.renderer_queue[0])