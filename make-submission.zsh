#!/bin/zsh

. ~/.zshrc

# init vars
id=3
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
cp -r reps $s
cp -r pymorph $s
each "rm $s/src/**/.*.\$1" swp swo
rm $s/src/**/*.pyc
rm $s/pymorph/*.pyc

zip -r submission $s/*

