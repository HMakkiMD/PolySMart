# run the relaxation after reaction
# $1 = i
# $2 = time
#source /usr/local/gromacs/bin/GMXRC

if [ $1 -eq 1 ]
then
	cp ../data/product_raw.itp ../product.itp
else
	echo 0 | gmx trjconv -f ../md/md$(($1-1)).xtc -s ../md/md$(($1-1)).tpr -o ../md/md$(($1-1)).gro -dump $2
	rm ../md/#md$(($1-1)).gro.1# > /dev/null 2>&1
	rm ../md/md$1.*** > /dev/null 2>&1
	rm ../loops/loop$1.txt > /dev/null 2>&1
	rm ../itp/loop$1.itp > /dev/null 2>&1
	cp ../itp/loop$(($1-1)).itp ../product.itp
fi
