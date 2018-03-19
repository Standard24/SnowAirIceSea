for file in *.tgd
do 
	# printf ${file:0:8}	
	./teqc +nav ${file:0:8}.nav +obs ${file:0:8}.obs $file
done
