# run a relaxation for system before entering loops
# $1 = threads
source /usr/local/gromacs/bin/GMXRC

cp ../product.itp ../data/product_raw.itp
mkdir ../loops
mkdir ../min
mkdir ../md
mkdir ../itp

gmx grompp -f ../data/martini_em.mdp -c ../data/box.gro -p ../topol.top -o ../min/min0.tpr -maxwarn 1
gmx mdrun -v -deffnm ../min/min0 -rdd 1.4 -nt $1
gmx grompp -f ../data/martini_eq.mdp -c ../min/min0.gro -p ../topol.top -o ../min/eq0.tpr
gmx mdrun -v -deffnm ../min/eq0 -rdd 1.4 -nt $1
gmx grompp -f ../data/martini_run.mdp -c ../min/eq0.gro -t ../min/eq0.cpt -p ../topol.top -o ../md/md0.tpr
gmx mdrun -v -deffnm ../md/md0 -rdd 1.4 -nt $1
cp ../md/md0.gro ../data/mixture_raw.gro