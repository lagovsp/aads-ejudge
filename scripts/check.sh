#!/bin/bash
# Copyright Sergey Lagov 2022

tests=$({ python3 test-limit.py "$3/dat/"; } 2>&1)

echo "            Time               $(date +"%Y-%m-%d %T")"
echo "        Language               $1"
echo "     Source path               $2"
echo "      Tests path               $3"

if [[ "$4" == "no" ]]; then
  echo "   Order matters               no"
else
  echo "   Order matters               yes"
fi

echo "           Tests               $tests"
echo

output="output.txt"
ofilename="test_program"

if [[ "$1" == "cpp" ]]; then
  g++ -o "$ofilename" "$2" -std=c++17 -g -O3 -fno-asm -lm
fi

for ((i = 1; i <= $tests; ++i)); do
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

  if [[ "$4" == "no" ]]; then
    python3 checker.py "$3"/ans/"$i".ans "$output" no
  else
    python3 checker.py "$3"/ans/"$i".ans "$output"
  fi
done

if [[ "$1" == "cpp" ]]; then
  rm "$ofilename"
fi
rm "$output"
