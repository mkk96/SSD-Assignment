#!/bin/bash
shellc()
{
	temparray=($(compgen -c| sort -u))
	temparraylength=${#temparray[@]}
	len=$1
	list=()
	for var in "${temparray[@]}"
	do
		if [[ ${#var} -eq len ]]
		then
			list+=($var)
		fi
	done
	echo "${list[@]}"
}
makehash()
{
	string=($(echo $1 | sed -e 's/\(.\)/\1\n/g'))
	length=${#string[@]}
	declare -A newmap
	for ((i=0;i<128;i++))
	do
		newmap[$i]=0
	done
	for ((i=0;i<length;i++))
	do
		charint=$(printf "%d" "'${string[$i]}'")
		let charint=$charint
		((newmap[$charint]++))
	done
	echo "${newmap[@]}"
}
input=$(echo "$1")
wordhash=($(makehash $input ))
len=${#1}
shellcommand=($(shellc $len))
commandlength=${#shellcommand[@]}
list=()
count=0
for var in "${shellcommand[@]}"
do
	commandhash=($(makehash $var ))
	flag=0
	for ((i=0;i<128;i++))
	do
		if [[ "${wordhash[$i]}" != "${commandhash[$i]}" ]]
		then
			flag=1
			break
		fi
	done
	if [[ flag -eq 0 ]]
	then
		list+=($var)
	fi
done
flag=${#list[@]}
if [[ $flag -ne 0 ]]
then
	printf "YES"
	len=${#list[@]}
	for((i=0;i<len;i++))
	do
		printf "\t%s" ${list[$i]}
	done
	echo
else
	echo NO
fi
