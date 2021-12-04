#!/bin/bash
array=($(grep -io '\b\w*\ING\b' $1))
arraylength=${#array[@]}
for (( i=0; i<${arraylength}; i++));
do
  echo "${array[$i]}" | tr '[:upper:]' '[:lower:]'
done > $2
