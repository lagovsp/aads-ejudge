#!/bin/bash
# Copyright Sergey Lagov 2022

echo "Language:            $1"
echo "Program source path: $2"
echo "Tests folder path:   $3"
echo "Tests:               $4"

output="output.txt"
ofilename="test_program"

if [[ "$1" == "cpp" ]]; then
  g++ -o "$ofilename" "$2" -std=c++17 -g -O3 -fno-asm -lm
fi

for ((i = 1; i <= $4; ++i)); do
  printf "Test %2s:" $i
  if ! [ -f "$3"/dat/"$i".dat ]; then
    echo "                       File $3/dat/$i.dat not found"
    continue
  fi
  start=$(($(date +%s%N) / 1000000))
  if [[ "$1" == "py" ]]; then
    T=$({ /usr/bin/time -f "%MKB" python3 "$2" >"$output" <"$3"/dat/"$i".dat; } 2>&1)
  fi
  if [[ "$1" == "cpp" ]]; then
    T=$({ /usr/bin/time ./"$ofilename" "$2" >"$output" <"$3"/dat/"$i".dat; } 2>&1)
  fi
  end=$(($(date +%s%N) / 1000000))
  runtime=$((end - start)) # milliseconds
  secs=$((runtime / 1000))
  milliseconds=$((runtime - secs * 1000))
  printf "%3s.%03ds               " $secs $milliseconds
  python3 checker.py "$3"/ans/"$i".ans "$output"
done

if [[ "$1" == "cpp" ]]; then
  rm "$ofilename"
fi
rm "$output"
