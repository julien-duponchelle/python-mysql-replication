#!/usr/bin/env bash

usage(){
    echo "Usage: bash .extract_charset_list.sh (mysql|mariadb) >> charset_list.csv"
}

dbms=$1
if [ -z "$dbms" ]; then
    usage
    exit 1
fi

SQL_QUERY="SELECT id, character_set_name, collation_name, is_default
FROM information_schema.collations ORDER BY id;"

mysql -N -s -e "$SQL_QUERY" | python3 -c "import sys
dbms = sys.argv[1]
for line in sys.stdin:
    _id, name, collation, is_default = line.split(chr(9))
    if _id == 'NULL':
        continue
    is_default = True if is_default.strip() == 'Yes' else False
    print(f'{_id},{name},{collation},{is_default},{dbms}')
" "$dbms"
