from collections import defaultdict
import os

class Charset:
    def __init__(self, id, name, collation, is_default=False, dbms='mysql'):
        self.id, self.name, self.collation = id, name, collation
        self.is_default = is_default
        self.dbms = dbms

    def __repr__(self):
        return (
            f"Charset(id={self.id}, name={self.name!r}, collation={self.collation!r})"
        )

    @property
    def encoding(self):
        name = self.name
        if name in ("utf8mb4", "utf8mb3"):
            return "utf8"
        if name == "latin1":
            return "cp1252"
        if name == "koi8r":
            return "koi8_r"
        if name == "koi8u":
            return "koi8_u"
        return name

    @property
    def is_binary(self):
        return self.id == 63


class Charsets:
    def __init__(self):
        self._by_id = defaultdict(dict)  # key: mysql / mariadb
        self._by_name = defaultdict(dict)  # key: mysql / mariadb

    def add(self, _charset):
        self._by_id[_charset.dbms][_charset.id] = _charset
        if _charset.is_default:
            self._by_name[_charset.dbms][_charset.name] = _charset

    def by_id(self, id, dbms='mysql'):
        return self._by_id.get(dbms, {}).get(id)

    def by_name(self, name, dbms='mysql'):
        if name == "utf8":
            name = "utf8mb4"
        return self._by_name.get(dbms, {}).get(name.lower())


charsets = Charsets()
charset_by_name = charsets.by_name
charset_by_id = charsets.by_id

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charset_list.csv'), 'r') as f:
    f.readline()  # pass header
    for line in f:
        lines = line.split(',')
        if len(lines) != 5:
            continue

        _id, _name, _collation, _is_default, _dbms = lines
        charsets.add(
            Charset(_id, _name, _collation, _is_default, _dbms)
        )
