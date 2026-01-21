# run a relaxation for system before entering loops
# $1 = threads
#source /usr/local/gromacs/bin/GMXRC

cp ../product.itp ../data/product_raw.itp
mkdir ../loops
mkdir ../min
mkdir ../md
mkdir ../itp

gmx grompp -f ../data/martini_run.mdp -c ../data/box.gro -p ../data/topol1.top -o ../md/md0.tpr -maxwarn 1
gmx mdrun -v -deffnm ../md/md0 -nt $1
cp ../md/md0.gro ../data/mixture_raw.gro
cp ../product.itp ../itp/loop0.itp
