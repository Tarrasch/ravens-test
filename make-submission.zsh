#!/bin/zsh

. ~/.zshrc

# init vars
id=2
pid="Project_$id"
name="ArashRouhani"
npid="${name}_${pid}"
s="submission"

# fresh dir, no zip
rm -rf $s
mkdir $s
rm submission.zip

# create and copy stuff over
pandoc README.markdown -o "$s/$npid.pdf"
cp -r src $s/src
cp main.py $s/$npid.py
mkdir $s/reps
mapl "cp \$1 $s/reps/${id}-\${1/yaml/txt}" ?.yaml
cp -r yaml $s
eachl "rm $s/src/**/.*.\$1" swp swo
rm $s/src/**/*.pyc
rm $s/yaml/*.pyc

zip -r submission $s/*

