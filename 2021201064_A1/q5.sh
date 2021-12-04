mkdir temp_activity
cd temp_activity
touch temp{1..50}.txt
for f in {1..25}
do 
    mv "temp"$f".txt" "temp"$f".md";
done
for f in temp*.*
do
	arrIN=(${f//./ })
	mv $f "${arrIN[0]}"_modified."${arrIN[1]}"
done
zip txt_compressed.zip *.txt > /dev/null 2>&1
