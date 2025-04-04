# run the relaxation after reaction
# $1 = i-1
# $2 = threads
# $3 = time
#source /usr/local/gromacs/bin/GMXRC
cp ../product.itp ../itp/loop$(($1+1)).itp
mkdir ../min  > /dev/null 2>&1
if [ -f "../md/md$(($1+1)).gro" ]; then
    rm ../md/md$(($1+1)).gro   > /dev/null 2>&1
fi
gmx grompp -f ../data/martini_em.mdp -c ../md/temp.gro -p ../topol.top -o ../min/min$(($1+1)).tpr -maxwarn 1
gmx mdrun -v -deffnm ../min/min$(($1+1)) -nt $2
gmx grompp -f ../data/martini_eqxl.mdp -c ../min/min$(($1+1)).gro -p ../topol.top -o ../md/md$(($1+1)).tpr
gmx mdrun -v -deffnm ../md/md$(($1+1)) -nt $2
if [ -f "../md/md$(($1+1)).gro" ]; then
    echo 0 | gmx trjconv -f ../md/md$(($1+1)).xtc -s ../md/md$(($1+1)).tpr -o ../md/md$(($1+1)).gro -dump $3
else 
    rm ../md/md$(($1+1)).*   > /dev/null 2>&1
    gmx grompp -f ../data/martini_eqxl1.mdp -c ../min/min$(($1+1)).gro -p ../topol.top -o ../md/eq$(($1+1)).tpr -maxwarn 1
	gmx mdrun -v -deffnm ../md/eq$(($1+1)) -nt $2
	gmx grompp -f ../data/martini_eqxl.mdp -c ../md/eq$(($1+1)).gro -p ../topol.top -o ../md/md$(($1+1)).tpr
	gmx mdrun -v -deffnm ../md/md$(($1+1)) -nt $2
	rm ../md/eq$(($1+1)).*   > /dev/null 2>&1
	echo 0 | gmx trjconv -f ../md/md$(($1+1)).xtc -s ../md/md$(($1+1)).tpr -o ../md/md$(($1+1)).gro -dump $3
fi
rm ../md/#md$(($1+1)).gro.1#  > /dev/null 2>&1
rm ../min/#min$(($1+1)).gro.1#  > /dev/null 2>&1
rm ../md/temp.gro  > /dev/null 2>&1
rm *.pdb > /dev/null 2>&1
