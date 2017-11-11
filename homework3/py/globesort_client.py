#!/usr/bin/env python
import argparse
import random
import sys

import grpc

import globesort_pb2
import globesort_pb2_grpc

def parse_args():
    parser = argparse.ArgumentParser(description="Globesort client")
    parser.add_argument("server_ip", type=str,
                        help="IP address of the server")
    parser.add_argument("server_port", type=int,
                        help="Port of the server")
    parser.add_argument("num_values", type=int,
                        help="Number of values to sort")
    return parser.parse_args()

def run(s_ip, s_port, vals):
    server_str = '%s:%d' % (s_ip, s_port)
    channel = grpc.insecure_channel(server_str)
    stub = globesort_pb2_grpc.GlobeSortStub(channel)

    print("Pinging %s..." % server_str)
    stub.Ping(globesort_pb2.Empty())
    print("Ping successful.")

    print("Requesting server to sort array...")
    response = stub.SortIntegers(globesort_pb2.IntArray(values=vals))
    print("Sorted array")


if __name__ == "__main__":
    args = parse_args()
    random.seed()
    values = [random.randint(-1000000000, 1000000000) for _ in range(args.num_values)]
    run(args.server_ip, args.server_port, values)
