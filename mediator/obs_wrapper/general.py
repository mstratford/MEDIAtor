from . import common

async def get_version():
  response = await common.connection.make_request('GetVersion')
  return response
