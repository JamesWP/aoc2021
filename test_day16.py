import collections
import functools
import operator

HEX = {
  '0' : '0000',
  '1' : '0001',
  '2' : '0010',
  '3' : '0011',
  '4' : '0100',
  '5' : '0101',
  '6' : '0110',
  '7' : '0111',
  '8' : '1000',
  '9' : '1001',
  'A' : '1010',
  'B' : '1011',
  'C' : '1100',
  'D' : '1101',
  'E' : '1110',
  'F' : '1111'
}

def hex_decode(hx):
  for c in hx:
    yield from HEX[c]

def read_number(bits, num_bits):
  value = 0
  for place in range(num_bits):
    value += (1 << num_bits - place) if bits.popleft() == '1' else 0
  return value >> 1

def read_vli(bits):
  value = 0
  while True:
    is_last = bits.popleft() == '0'
    value = value << 4
    value += read_number(bits, 4)

    if is_last:
      break

  return value

def parse_header(bits):
  version = read_number(bits, 3)
  type_id = read_number(bits, 3)

  return version, type_id

def parse_packet(bits):
  version, type_id = parse_header(bits)

  if type_id == 4:
    # literal value
    value = read_vli(bits)
    return version, type_id, value
 
  length_type_id = bits.popleft()

  sub_packets = []
  
  if length_type_id == '0':
    # length in bits
    total_bit_length = read_number(bits, 15)
    len_after_parse = len(bits) - total_bit_length

    while len_after_parse != len(bits):
      sub_packets.append(parse_packet(bits))
  else:
    num_sub_packets = read_number(bits, 11)
    for _ in range(num_sub_packets):
      sub_packets.append(parse_packet(bits))

  return version, type_id, sub_packets


def test_hex_decode():
  assert ''.join(hex_decode('D2FE28')) == '110100101111111000101000'

def test_parse_header():
  assert (6, 4) == parse_header(collections.deque(hex_decode('D2FE28')))

def test_parse_literal():
  (ver, type_id, v) = parse_packet(collections.deque(hex_decode('D2FE28')))
  assert v == 2021
   
def test_parse_operator():
  (v, t, (a, b)) = parse_packet(collections.deque(hex_decode('38006F45291200'))) 

  assert (1,6) == (v,t)
  assert (6,4,10) == a
  assert (2,4,20) == b

  (v,t, (a, b, c)) = parse_packet(collections.deque(hex_decode('EE00D40C823060')))
  
  assert (7,3) == (v,t) 
  assert (2,4,1) == a
  assert (4,4,2) == b
  assert (1,4,3) == c

def test_part1():
  with open("input16.txt") as data:
    bits = collections.deque(hex_decode(data.read().strip()))

  def version_sum(packet):
    ver, type_id, val = packet

    if type_id == 4:
      return ver
    
    return ver + sum(version_sum(sub_packet) for sub_packet in val)

  assert version_sum(parse_packet(bits)) == 1038

TESTS = (
  ('C200B40A82', 3),
  ('04005AC33890', 54),
  ('880086C3E88112', 7),
  ('CE00C43D881120', 9),
  ('D8005AC2A8F0', 1),
  ('F600BC2D8F', 0),
  ('9C005AC2F8F0',0),
  ('9C0141080250320F1802104A08',1)
)

def evaluate(packet):
  ver, type_id, val = packet

  if type_id == 4:
    return val
  
  if type_id == 0:
    return sum(evaluate(p) for p in val)

  if type_id == 1:
    return functools.reduce(operator.mul, (evaluate(p) for p in val), 1)

  if type_id == 2:
    return min(evaluate(p) for p in val)

  if type_id == 3:
    return max(evaluate(p) for p in val)

  if type_id == 5:
    (a, b) = (evaluate(p) for p in val)
    return 1 if a > b else 0

  if type_id == 6:
    (a, b) = (evaluate(p) for p in val)
    return 1 if a < b else 0

  if type_id == 7:
    (a, b) = (evaluate(p) for p in val)
    return 1 if a == b else 0

def test_part00():
  for packet_hex, correct_value in TESTS:
    bits = collections.deque(hex_decode(packet_hex))
    assert evaluate(parse_packet(bits)) == correct_value

def test_part2():
  with open("input16.txt") as data:
    bits = collections.deque(hex_decode(data.read().strip()))

  assert evaluate(parse_packet(bits)) == 123
