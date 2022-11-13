#!/bin/bash
# Copyright Sergey Lagov 2022

echo Python script path: "$1"
echo Tests folder path: "$2"
echo Tests: "$3"

output="output.txt"

for ((i = 1; i <= $3; ++i)); do
  printf "Test %2s:" $i
  if ! [ -f "$2"/dat/"$i".dat ]; then
    echo "                       File $2/dat/$i.dat not found"
    continue
  fi

  start=$(($(date +%s%N) / 1000000))
  T=$({ /usr/bin/time -f "%MKB" python3 "$1" >"$output" <"$2"/dat/"$i".dat; } 2>&1)
  end=$(($(date +%s%N) / 1000000))
  runtime=$((end - start)) # milliseconds
  secs=$((runtime / 1000))
  milliseconds=$((runtime - secs * 1000))
  printf "%3s." $secs
  printf "%03ds %13s " $milliseconds $T
  python3 checker.py "$2"/ans/"$i".ans output.txt
done

rm "$output"
