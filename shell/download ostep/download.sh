while read -r dest src; do
    
powershell curl -o "$dest" "$src"   
done < file.txt

