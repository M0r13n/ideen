#!/usr/bin/env python3
import dataclasses
import itertools
import socket
import struct


def ntob(name):
    """Name to bytes"""
    bytes = bytearray()
    for part in name.split('.'):
        part = part.strip('.')
        bytes.append(len(part))
        bytes += part.encode('latin1')
    bytes.append(0)
    return bytes


def btos(bytes, start=0):
    """"
    Bytes to string.
    Parsed according to RFC-1035:
        The domain name terminates with the zero length octet 
        for the null label of the root. Note that this field
        may be an odd number of octets; no padding is used.

    Returns the parsed name + the index where parsing stopped
    """
    name = ''

    end=start
    while start < len(bytes):
        if bytes[start] == 0:
            break

        if bytes[start] & 0xc0:
            # TODO
            pass

        end = start+bytes[start]
        start += 1
        q = bytes[start:end+1].decode('latin1') + '.'
        name += q
        start = end + 1
    return name, start


@dataclasses.dataclass
class DNSFlags:
    # 2 bytes total
    qr: int = 0
    op: int = 0
    op_code: int = 0
    aa: int = 0
    tc: int = 0
    rd: int = 0
    ra: int = 0
    z: int = 0
    rcode: int = 0

    def asint(self) -> int:
        i = self.qr << 15
        i |= self.op_code << 11
        i |= self.aa << 10
        i |= self.tc << 9
        i |= self.rd << 8
        i |= self.ra << 7
        i |= self.z << 4
        i |= self.rcode
        return i

    @classmethod
    def fromint(cls, i):
        self = DNSFlags()
        self.qr = i & 0x8000
        self.op = (i >> 11) & 0x000f
        self.op_code = i & 0x0400
        self.aa = i & 0x0400
        self.tc = i & 0x0200
        self.rd = i & 0x0100
        self.ra = i & 0x0080
        # z is reserved and simply omitted (implicitly set to 0)
        self.rcode = i & 0x000f
        return self


@dataclasses.dataclass
class DNSHeader:
    # each entry has two bytes
    identifier: int = 0x1337
    flags: DNSFlags = DNSFlags()
    qd_count: int = 0
    an_count: int = 0
    ns_count: int = 0
    ar_count: int = 0

    def pack(self):
        return struct.pack(
            '>6H', self.identifier, self.flags.asint(), self.qd_count,
            self.an_count, self.ns_count, self.ar_count
        )

    @classmethod
    def unpack(cls, packed):
        args = struct.unpack('>6H', packed)
        identifier, flags, qd_count, an_count, ns_count, ar_count = args
        return cls(
            identifier, DNSFlags.fromint(flags),
            qd_count, an_count, ns_count, ar_count
        )


@dataclasses.dataclass
class DNSQuestion:
    qname: str  # N bytes. No padding
    qtype: int = 1  # 2 bytes. A-record = 1
    qclass: int = 1  # 2 bytes. Query IN = 1

    def pack(self):
        bytes = ntob(self.qname)
        bytes += struct.pack('!HH', self.qtype, self.qclass)
        return bytes

    @classmethod
    def unpack(cls, packed):
        qname, ix_start = btos(packed)
        ix_end = ix_start+5
        qtype, qclass = struct.unpack('!HH', packed[ix_start + 1: ix_end])
        self = cls(qname, qtype, qclass)
        return self, ix_end


@dataclasses.dataclass
class ResourceRecord:
    name: str # N bytes
    rtype: int # 2 bytes
    rclass: int # 2 bytes
    ttl:int # 2 bytes
    rdata : str # N bytes

    @classmethod
    def unpack(cls, packed, ix_start):

        name, ix_start = btos(packed, ix_start)
        print(name)

        return None, 1


    


@dataclasses.dataclass
class DNSMessage:
    header: DNSHeader = DNSHeader()
    questions: list = dataclasses.field(default_factory=list)
    answers: list = dataclasses.field(default_factory=list)
    authorities: list = dataclasses.field(default_factory=list)
    additional: list = dataclasses.field(default_factory=list)

    def pack(self):
        header = self.header.pack()
        payload = bytearray()
        for item in itertools.chain(self.questions, self.answers, self.authorities, self.additional):
            payload += item.pack()

        return header + payload

    @classmethod
    def unpack(cls, packed):
        self = cls()

        header = DNSHeader.unpack(packed[:12])
        self.header = header
        ix_end = 12

        qd_count = header.qd_count
        for _ in range(qd_count):
            question, ix_end = DNSQuestion.unpack(packed[ix_end:])
            self.questions.append(question)

        # TODO: continue here
        for _ in range(header.an_count):
            pass

        for _ in range(header.ns_count):
            record, ix_end = ResourceRecord.unpack(packed, ix_end + 1)
            print(record)

        for _ in range(header.ar_count):
            pass

        return self


def send_udp_msg(msg, addr, port):
    server_address = (addr, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(msg, server_address)
        data, _ = sock.recvfrom(4096)
    finally:
        sock.close()
    return data


if __name__ == '__main__':
    question = DNSQuestion('foo.de')
    msg = DNSMessage(header=DNSHeader(qd_count=1), questions=[question, ])
    packed = msg.pack()

    response = send_udp_msg(packed, '10.0.10.254', 53)

    answer = DNSMessage.unpack(response)

    print(answer)
