#!/bin/bash
converIntToRoman()
{
	number=(1000 900 500 400 100 90 50 40 10 9 5 4 1)
	numberR=(M CM D CD C XC L XL X IX V IV I)
	list=()
	length=${#number[@]}
	num=$1
	for (( i=0; i<${length}; i++ ))
	do
		while [[ $num -ge "${number[$i]}" ]]
		do
			list+=("${numberR[$i]}")
			num="$(($num - "${number[$i]}"))"

		done
	done 
	echo "${list[@]}"
}
convertRomanToInt()
{
	string=($(echo $1 | sed -e 's/\(.\)/\1\n/g'))
	length=${#string[@]}
	declare -A newmap
	newmap[I]=1
	newmap[V]=5
	newmap[X]=10
	newmap[L]=50
	newmap[C]=100
	newmap[D]=500
	newmap[M]=1000
	newmap[i]=1
	newmap[v]=5
	newmap[x]=10
	newmap[l]=50
	newmap[c]=100
	newmap[d]=500
	newmap[m]=1000
	result=${newmap[${string[$length - 1]}]}
	for (( i=$length-2;i>=0;i--))
	do
		if [[ ${newmap[${string[$i]}]} -lt ${newmap[${string[$i+1]}]} ]]
		then
			result="$(($result - "${newmap[${string[$i]}]}"))"
		else
			result="$(($result + "${newmap[${string[$i]}]}"))"
		fi
	done
	echo $result
}
pattern='^M?M?M?(CM|CD|D?C?C?C?)(XC|XL|L?X?X?X?)(IX|IV|V?I?I?I?)$' 
re='^[+-]?[0-9]+$'
if [ "$#" -gt 2 ] || [ "$#" -eq 0 ]
then
	echo Wrong number of Argument
else
	if [ "$#" -eq 1 ]
	then
		if [[ $1 =~ $re ]]
		then
			if [[ $1 -gt 3999 ]] || [[ $1 -lt 1 ]]
			then 
				echo Roman number not possible AS number is greater than 3999 or less than 1
			else
				var=($( converIntToRoman $1 ))
				printf %s "${var[@]}" $'\n'
			fi
		elif [[ $1 =~ $pattern ]]
		then		
			var=($( convertRomanToInt $1 ))
			echo $var
		else
			echo Not a valid roman Number or Integer
		fi
	else
		if [[ $1 =~ $re ]] && [[ $2 =~ $re ]]
		then
				num="$(($1 + $2))"
				if [[ $num -gt 3999 ]] || [[ $num -lt 1 ]]
				then 
					echo Sum is greater than 3999 or less than 1 not able represent in Roman
				else
					var=($( converIntToRoman $num ))
					printf %s "${var[@]}" $'\n'
				fi
		elif [[ $1 =~ $pattern ]] && [[ $2 =~ $pattern ]]
		then
			num1=($( convertRomanToInt $1 ))
			num2=($( convertRomanToInt $2 ))
			num="$(($num1 + $num2))"
			echo $num
			
		else
			echo One or more argument is not a Valid roman number or integer
		fi
	fi
fi
