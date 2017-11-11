#!/usr/bin/env python
from concurrent import futures
import argparse
import time

import grpc

import globesort_pb2
import globesort_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class GlobeSort(globesort_pb2_grpc.GlobeSortServicer):

    def Ping(self, request, context):
        return globesort_pb2.Empty()

    def SortIntegers(self, request, context):
        return globesort_pb2.IntArray(values=sorted(request.values))


def parse_args():
    parser = argparse.ArgumentParser(description="Globesort server")
    parser.add_argument("server_port", type=int, default=None,
                        help="Port to run the server on")
    parser.add_argument("-a", "--address", type=str, default="0.0.0.0",
                        help="IP to bind the server to")
    return parser.parse_args()


def serve(address, server_port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    globesort_pb2_grpc.add_GlobeSortServicer_to_server(GlobeSort(), server)
    server.add_insecure_port('%s:%d' % (address, server_port))
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    args = parse_args()
    serve(args.address, args.server_port)
