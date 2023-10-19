#!/usr/bin/env bash

set -e
set -x

ruff pymysqlreplication
black pymysqlreplication --exclude pymysqlreplication/bitmap.py --check
