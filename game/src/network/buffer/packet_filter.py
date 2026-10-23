'''
The packet console's filter: a line of text that the Filters overlay's
checkboxes and comboboxes write, a lesson can hand out to paste in, and an
advanced student can type by hand.

    proto:modbus,tcp dir:in -host:"Attacker Pi"

  - field:value matches packets whose field is that value. Several values,
    split by commas, match any of them (OR).
  - Terms side by side must all match (AND) - "and" may be written out.
  - -term (or "not term") matches packets the term doesn't.
  - "or" and parentheses combine terms any other way.
  - A bare word searches the packet's Info and Summary, addresses and
    protocol.
  - Values with spaces, commas, parentheses or quotes go in "quotes".

That's the checkboxes' own rule - OR within a field, AND between fields,
"-" for an option ticked to leave out - written out (see conjugate), so a
filter in that form reads back into them (see to_state). Anything else
("or", parentheses, bare words, a field given twice) still filters; the
overlay just can't show it in its boxes.

FIELDS lists every field the overlay offers, by section. Host values match
part of an IP or MAC address, or of a nickname from Configure Hosts
(Preferences.host_nicknames); a pair is two hosts, "A<>B", matching traffic between them
either way (an empty side matches anyone); register values match a register
(hreg_4), or part of its nickname (modbus_registers).
'''
import re
from dataclasses import dataclass
from typing import Callable

TRUE_WORDS = {"true", "yes", "1", "on"}
FALSE_WORDS = {"false", "no", "0", "off"}


@dataclass(frozen=True)
class Field:
    name: str                      # as it's typed: "src", "modbus.type"
    section: str                   # see SECTIONS
    kind: str                      # "check" (its values are checkboxes) or "combo" (any text, in comboboxes)
    values: tuple[str, ...] = ()   # a "check" field's values, in the overlay's order


SECTIONS = ("hosts", "type", "modbus", "meta")
FIELDS: list[Field] = [
    Field("dst", "hosts", "combo"),
    Field("src", "hosts", "combo"),
    Field("host", "hosts", "combo"),
    Field("pair", "hosts", "combo"),
    Field("to", "hosts", "check", ("broadcast",)),
    Field("proto", "type", "check", ("tcp", "udp", "icmp", "arp", "dns", "dhcp", "http", "https", "modbus", "ipv6",
                                     "wifi", "eapol", "stp", "lldp", "cdp")),
    Field("icmp", "type", "check", ("ping", "reply", "unreachable", "expired")),
    Field("arp", "type", "check", ("request", "reply", "gratuitous")),
    Field("wifi", "type", "check", ("beacon", "probe", "auth", "assoc", "deauth", "handshake")),
    Field("modbus", "modbus", "check", ("true",)),
    Field("modbus.type", "modbus", "check", ("request", "response")),
    Field("modbus.command", "modbus", "check", ("read", "write")),
    Field("modbus.full", "modbus", "check", ("read-request", "read-response", "write-request", "write-response")),
    Field("modbus.reg", "modbus", "combo"),
    Field("modbus.consequential", "modbus", "check", ("true", "false")),
    Field("modbus.first", "modbus", "check", ("true", "false")),
    Field("observer", "meta", "check", ("sniff", "arp", "dos", "nfq", "nmap", "pcap")),
    Field("dir", "meta", "check", ("in", "out", "other")),
    Field("side", "meta", "check", ("before", "after")),
]
BY_NAME: dict[str, Field] = {field.name: field for field in FIELDS}
# Other names a field may be typed as
ALIASES = {"either": "host", "pairs": "pair", "protocol": "proto", "hack": "observer", "direction": "dir",
           "reg": "modbus.reg", "register": "modbus.reg"}


class FilterError(ValueError):
    '''A filter that can't be read - its message says why, for the overlay to show.'''


# Reading text
def tokenize(text: str) -> list[str]:
    '''Words, "(" and ")" - a word runs to whitespace or a parenthesis, but takes in anything inside "quotes".'''
    tokens, i = [], 0
    while i < len(text):
        char = text[i]
        if char.isspace():
            i += 1
        elif char in "()":
            tokens.append(char)
            i += 1
        else:
            start = i
            while i < len(text) and not text[i].isspace() and text[i] not in "()":
                if text[i] == '"':
                    i += 1
                    while i < len(text) and text[i] != '"':
                        i += 2 if text[i] == "\\" else 1
                    if i >= len(text):
                        raise FilterError('A quote (") isn\'t closed.')
                i += 1
            tokens.append(text[start:i])
    return tokens


def split_outside_quotes(word: str, separator: str, limit: int = -1) -> list[str]:
    parts, current, quoted, i = [], "", False, 0
    while i < len(word):
        char = word[i]
        if char == "\\" and quoted and i + 1 < len(word):
            current += word[i:i + 2]
            i += 2
            continue
        if char == '"':
            quoted = not quoted
        if char == separator and not quoted and limit != 0:
            parts.append(current)
            current = ""
            limit -= 1
        else:
            current += char
        i += 1
    parts.append(current)
    return parts


def unquote(text: str) -> str:
    if len(text) >= 2 and text[0] == text[-1] == '"':
        return re.sub(r"\\(.)", r"\1", text[1:-1])
    return text


def quote(value: str) -> str:
    '''value as it's written in a filter - in quotes if it would otherwise read as something else.'''
    if value and re.fullmatch(r'[^\s(),"]+', value) and value.lower() not in ("or", "and", "not"):
        return value
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def normal_value(field: Field, value: str) -> str:
    '''A typed value as the field's own spelling - lower-case for a checkbox field, true/false for yes/no/1/0.'''
    if field.kind == "combo":
        return value
    value = value.lower()
    if value in TRUE_WORDS and ("true" in field.values or field.values == ("true",)):
        return "true"
    if value in FALSE_WORDS and ("false" in field.values or field.values == ("true",)):
        return "false"
    return value


class Parser:
    '''
    filter := either
    either := both ("or" both)*
    both   := one (["and"] one)*
    one    := ("not" | "-") one  |  "(" either ")"  |  word
    '''

    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.at = 0

    def peek(self) -> str | None:
        return self.tokens[self.at] if self.at < len(self.tokens) else None

    def take(self) -> str:
        token = self.tokens[self.at]
        self.at += 1
        return token

    def either(self):
        parts = [self.both()]
        while (self.peek() or "").lower() == "or":
            self.take()
            parts.append(self.both())
        return parts[0] if len(parts) == 1 else ("or", parts)

    def both(self):
        parts = [self.one()]
        while self.peek() is not None and self.peek() != ")" and self.peek().lower() != "or":
            if self.peek().lower() == "and":
                self.take()
            parts.append(self.one())
        return parts[0] if len(parts) == 1 else ("and", parts)

    def one(self):
        token = self.peek()
        if token is None or token == ")" or token.lower() in ("or", "and"):
            raise FilterError(f"Expected a term {'at the end' if token is None else f'before {token!r}'}.")
        self.take()
        if token.lower() == "not":
            return ("not", self.one())
        if token == "(":
            inside = self.either()
            if self.peek() != ")":
                raise FilterError("A parenthesis isn't closed.")
            self.take()
            return inside
        if token.startswith(("-", "!")) and len(token) > 1:
            return ("not", self.word(token[1:]))
        return self.word(token)

    @staticmethod
    def word(token: str):
        parts = split_outside_quotes(token, ":", limit=1)
        if len(parts) == 1 or parts[0].startswith('"'):
            text = unquote(token)
            if not text:
                raise FilterError("An empty search.")
            return ("text", text)
        name = ALIASES.get(parts[0].lower(), parts[0].lower())
        field = BY_NAME.get(name)
        if field is None:
            raise FilterError(f"There's no field called {parts[0]!r}.")
        values = [normal_value(field, unquote(value)) for value in split_outside_quotes(parts[1], ",")]
        if not values or any(value == "" for value in values):
            raise FilterError(f"{field.name}: needs a value after it.")
        if field.kind == "check":
            allowed = field.values + (("false",) if field.values == ("true",) else ())
            for value in values:
                if value not in allowed:
                    raise FilterError(f"{field.name}: can be {', '.join(allowed)} - not {value!r}.")
        return ("term", field.name, tuple(values))


def parse(text: str):
    '''The filter's tree - ("and"|"or", [parts]), ("not", part), ("term", field, values), ("text", word) - or None if empty.'''
    tokens = tokenize(text)
    if not tokens:
        return None
    parser = Parser(tokens)
    tree = parser.either()
    if parser.peek() is not None:
        raise FilterError(f"Unexpected {parser.peek()!r}." if parser.peek() == ")" else "Couldn't read the filter.")
    return tree


# The checkboxes' state <-> text
def empty_state() -> dict[str, dict[str, list[str]]]:
    return {field.name: {"include": [], "exclude": []} for field in FIELDS}


def to_state(tree) -> dict[str, dict[str, list[str]]] | None:
    '''
    What the overlay's boxes show for a filter: each field's included and
    excluded values. None if the boxes can't show it - "or", parentheses,
    a bare word, or a field included twice (which ANDs, where a field's
    boxes OR).
    '''
    state = empty_state()
    if tree is None:
        return state
    parts = tree[1] if tree[0] == "and" else [tree]
    included = set()
    for part in parts:
        negated = part[0] == "not"
        term = part[1] if negated else part
        if term[0] != "term":
            return None
        _, name, values = term
        if name == "modbus":
            # Its one box: "true" ticked in, or "false" - ticked out
            flipped = negated != (values == ("false",))
            if set(values) != {"true"} and set(values) != {"false"}:
                return None
            negated, values = flipped, ("true",)
        if negated:
            state[name]["exclude"] += [value for value in values if value not in state[name]["exclude"]]
        else:
            if name in included:
                return None
            included.add(name)
            state[name]["include"] = list(dict.fromkeys(values))
    return state


def conjugate(state: dict[str, dict[str, list[str]]]) -> str:
    '''The filter text for a state of the boxes, in FIELDS order: field:values for those ticked in, -field:values for those ticked out.'''
    terms = []
    for field in FIELDS:
        entry = state.get(field.name) or {}
        include, exclude = entry.get("include") or [], entry.get("exclude") or []
        if field.name == "modbus":
            if include:
                terms.append("modbus:true")
            elif exclude:
                terms.append("modbus:false")
            continue
        if include:
            terms.append(f"{field.name}:{','.join(map(quote, include))}")
        if exclude:
            terms.append(f"-{field.name}:{','.join(map(quote, exclude))}")
    return " ".join(terms)


# Matching packets
PAIR_SEPARATOR = "<>"


def split_pair(value: str) -> tuple[str, str]:
    '''A pair value's two hosts - "A<>B" is ("A", "B"); one without the separator is one host, talking to anyone.'''
    first, _, second = value.partition(PAIR_SEPARATOR)
    return first.strip(), second.strip()


def join_pair(first: str, second: str) -> str:
    return f"{first.strip()}{PAIR_SEPARATOR}{second.strip()}"


def is_broadcast(mpkt) -> bool:
    '''Sent to everyone on the network (broadcast) or to a group (multicast).'''
    mac = str(mpkt.get("mac_dst") or "").lower()
    ip = str(mpkt.get("ip_dst") or "").lower()
    if mac == "ff:ff:ff:ff:ff:ff" or mac.startswith(("01:00:5e", "33:33", "01:80:c2")):
        return True
    if ip == "255.255.255.255" or ip.startswith("ff"):
        return True
    first = ip.split(".")[0]
    return (first.isdigit() and 224 <= int(first) <= 239) or (ip.count(".") == 3 and ip.endswith(".255"))


def compile_filter(tree, context) -> Callable[[object], bool]:
    '''A function telling whether a MetaPacket passes the filter. A packet the filter trips over doesn't.'''
    if tree is None:
        return lambda mpkt: True
    states = context.states

    def nickname(mac: str) -> str:
        return context.preferences.host_nickname(mac).lower()

    def end_matches(value: str, ip: str, mac: str) -> bool:
        value = value.lower()
        return any(value in str(address).lower() for address in (ip, mac) if address and address != "-") \
            or (mac not in ("", "-") and value in nickname(mac))

    def end(mpkt, side: str) -> tuple[str, str]:
        return str(mpkt.get(f"ip_{side}") or "-"), str(mpkt.get(f"mac_{side}") or "-")

    def register_matches(value: str, variables: list) -> bool:
        value = value.lower()
        if re.fullmatch(r"hreg_\d+", value):
            return value in variables
        registers = states.get("modbus_registers")
        return any(value in variable or value in str((registers.get(variable) or {}).get("nickname") or "").lower()
                   for variable in variables)

    def modbus_command(mpkt) -> str:
        command = str(mpkt.get("command") or "").lower()
        return "read" if "read" in command else "write" if "write" in command else ""

    def boolean(value) -> str:
        return "true" if value in (True, 1, "1", "true") else "false"

    def has_layer(prefixes: tuple[str, ...]):
        return lambda mpkt: any(str(layer).startswith(prefixes) for layer in mpkt.get("layers") or [])

    protocols = {
        "tcp": has_layer(("TCP",)), "udp": has_layer(("UDP",)), "icmp": has_layer(("ICMP",)), "arp": has_layer(("ARP",)),
        "dns": has_layer(("DNS",)), "dhcp": has_layer(("DHCP", "BOOTP")), "ipv6": has_layer(("IPV6",)),
        "modbus": has_layer(("MODBUS",)), "wifi": has_layer(("DOT11", "RADIOTAP")), "eapol": has_layer(("EAPOL",)),
        "stp": has_layer(("STP",)), "cdp": has_layer(("CDP",)),
        "lldp": lambda mpkt: mpkt.described("protocol") == "LLDP",
        "http": lambda mpkt: mpkt.described("service") == "HTTP",
        "https": lambda mpkt: mpkt.described("service") == "HTTPS",
    }
    sides = {"before": "prerouting nfq", "after": "postrouting nfq"}

    # field -> (packet, value) -> whether it matches; a term matches if any of its values does
    matchers: dict[str, Callable] = {
        "dst": lambda mpkt, value: end_matches(value, *end(mpkt, "dst")),
        "src": lambda mpkt, value: end_matches(value, *end(mpkt, "src")),
        "host": lambda mpkt, value: end_matches(value, *end(mpkt, "src")) or end_matches(value, *end(mpkt, "dst")),
        "to": lambda mpkt, value: is_broadcast(mpkt),
        "proto": lambda mpkt, value: protocols[value](mpkt),
        "icmp": lambda mpkt, value: f"icmp:{value}" in (mpkt.described("tags") or []),
        "arp": lambda mpkt, value: f"arp:{value}" in (mpkt.described("tags") or []),
        "wifi": lambda mpkt, value: f"wifi:{value}" in (mpkt.described("tags") or []),
        "modbus": lambda mpkt, value: boolean(mpkt.get("is_modbus")) == value,
        "modbus.type": lambda mpkt, value: str(mpkt.get("command_type") or "").lower() == value,
        "modbus.command": lambda mpkt, value: modbus_command(mpkt) == value,
        "modbus.full": lambda mpkt, value: f"{modbus_command(mpkt)}-{str(mpkt.get('command_type') or '').lower()}" == value,
        "modbus.reg": lambda mpkt, value: register_matches(value, mpkt.get("variables") or []),
        "modbus.consequential": lambda mpkt, value: boolean(mpkt.get("is_useful")) == value,
        "modbus.first": lambda mpkt, value: boolean(mpkt.get("is_primary")) == value,
        "observer": lambda mpkt, value: mpkt.get("hack") == value,
        "dir": lambda mpkt, value: mpkt.get("direction") == value,
        "side": lambda mpkt, value: mpkt.get("observer") == sides[value],
    }

    def build(node) -> Callable:
        kind = node[0]
        if kind == "and":
            parts = [build(part) for part in node[1]]
            return lambda mpkt: all(part(mpkt) for part in parts)
        if kind == "or":
            parts = [build(part) for part in node[1]]
            return lambda mpkt: any(part(mpkt) for part in parts)
        if kind == "not":
            inner = build(node[1])
            return lambda mpkt: not inner(mpkt)
        if kind == "text":
            word = node[1].lower()
            return lambda mpkt: any(word in str(mpkt.described(key) or "").lower()
                                    for key in ("info", "summary", "src", "dst", "protocol"))
        _, name, values = node
        if name == "pair":
            # Each value is two hosts, "A<>B": traffic between them, either way
            ends = [split_pair(value) for value in values]

            def between(mpkt, first: str, second: str) -> bool:
                src, dst = end(mpkt, "src"), end(mpkt, "dst")
                def side(value, address):
                    return not value or end_matches(value, *address)
                return (side(first, src) and side(second, dst)) or (side(second, src) and side(first, dst))
            return lambda mpkt: any(between(mpkt, first, second) for first, second in ends)
        match = matchers[name]
        return lambda mpkt: any(match(mpkt, value) for value in values)

    test = build(tree)

    def packet_filter(mpkt) -> bool:
        try:
            return test(mpkt)
        except Exception as error:
            print(f"Packet filter failed on packet {mpkt.get('number')}: {error!r}")
            return False
    return packet_filter
