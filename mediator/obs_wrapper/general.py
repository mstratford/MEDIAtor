from .common import make_request

async def get_version():

  response = await make_request('GetVersion')
  return response
