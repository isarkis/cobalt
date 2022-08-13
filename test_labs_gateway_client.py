"""gRPC Test Labs Gateway server."""
from __future__ import print_function
import grpc
import test_labs_gateway_pb2
import test_labs_gateway_pb2_grpc
import sys

_WORK_DIR = '/test_labs_gateway'
_TEST_LABS_GATEWAY_SERVICE_HOST = 'test-labs-gateway-service'
_TEST_LABS_GATEWAY_SERVICE_PORT = '50051'


class TestLabsGatewayClient():
  """Test Labs Gateway Client class."""

  def __init__(self):
    self.channel = grpc.insecure_channel(
      target='%s:%s' %
        (_test_labs_GATEWAY_SERVICE_HOST,
         _test_labs_GATEWAY_SERVICE_PORT),
      # These options need to match server settings.
      options=[
        ('grpc.keepalive_time_ms', 10000),
        ('grpc.keepalive_timeout_ms', 5000),
        ('grpc.keepalive_permit_without_calls', 1),
        ('grpc.http2.max_pings_without_data', 0),
        ('grpc.http2.min_time_between_pings_ms', 10000),
        ('grpc.http2.min_ping_interval_without_data_ms', 5000)
      ]
    )
    self.stub = test_labs_gateway_pb2_grpc.test_labs_gatewayStub(
        self.channel)

  def run_command(self, workdir, args):
    for response_line in self.stub.exec_command(
        test_labs_gateway_pb2.TestLabsCommand(
            workdir=workdir, args=args)):
      print(response_line.response, end='')


def main():
  """Main routine."""
  client = TestLabsGatewayClient()
  try:
    cmd = ' '.join(sys.argv[1:])
    client.run_command(workdir=_WORK_DIR, args=cmd)
  except grpc.RpcError as e:
    print(e)
    return e.code().value


if __name__ == '__main__':
  sys.exit(main())
