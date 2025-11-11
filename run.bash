#!/bin/bash

echo "================="
echo "Generiranje"
echo "================="
python3 GSA.py < ulaz.txt > izlaz.txt
echo "================="
echo "ANALIZIRANJE"
echo "================="
cd analizator
python3 SA.py < ulaz.txt > izlaz.txt