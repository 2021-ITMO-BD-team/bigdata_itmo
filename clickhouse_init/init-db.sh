#!/bin/bash
set -e

clickhouse client -n <<-EOSQL
    CREATE DATABASE docker;
EOSQL