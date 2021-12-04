du -sh */ 2>&1 | grep -v '^du:' | sort -h -r| tr -d / | awk '{for(i=2;i<=NF;i++){printf "%s\t", $i};printf "%s\n",$1}'
