from __future__ import print_function
import pkg_resources
import os, sys, ctypes

lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'srb-shared.dll')
lib = ctypes.cdll.LoadLibrary(lib_path)

def create(name, size, num):
  ctx = ctypes.c_void_p()
  ctx_ptr = ctypes.pointer(ctx)
  #c_name = ctypes.c_char_p(name)
  c_size = ctypes.c_int32(size)
  c_num = ctypes.c_int32(num)
  if lib.shared_ring_buffer_create(ctx_ptr, name.encode('utf-8'), c_size, c_num) != 0:
    raise Exception('Fail to create the SharedRingBuffer!')
  return SharedRingBuffer(ctx)

def open(name):
  ctx = ctypes.c_void_p()
  ctx_ptr = ctypes.pointer(ctx)
  #c_name = ctypes.c_char_p(name)
  if lib.shared_ring_buffer_open(ctx_ptr, name.encode('utf-8')) != 0:
    raise Exception('Fail to open the SharedRingBuffer!')
  return SharedRingBuffer(ctx)

class SharedRingBuffer:
  def __init__(self, ctx):
    self.ctx = ctx
  
  def __del__(self):
    lib.shared_ring_buffer_close(self.ctx)
  
  def read(self, size):
    c_size = ctypes.c_int32(size)
    c_buf = ctypes.create_string_buffer(size)
    if not bool(lib.shared_ring_buffer_read(self.ctx, c_buf, c_size)):
      raise Exception('Fail to read data.')
    return bytearray(c_buf.raw)

  def write(self, buf, size):
    #c_buf = (ctypes.c_ubyte * size)(*buf)
    c_buf = ctypes.cast(buf, ctypes.c_char_p)
    c_size = ctypes.c_int(size)
    if not bool(lib.shared_ring_buffer_write(self.ctx, c_buf, c_size)):
      raise Exception('Fail to write data.')
