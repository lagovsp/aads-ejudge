#!/bin/bash
# Copyright Sergey Lagov 2022

echo Python script path: "$1"
echo Tests folder path: "$2"
echo Tests: "$3"

for ((i = 1; i <= $3; ++i)); do
  python3 "$1" >output.txt <"$2"/input/input"$i".txt
  echo -n "Test $i: "
  python3 checker.py output.txt "$2"/answers/answer"$i".txt
done
