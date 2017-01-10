#!/bin/bash

# Trasnform file 1 csv with ";" into file 2 csv with ","

if test $# -eq 2 
then 
sed -e "s/;/,/g" $1 > $2

else 
echo "Vous devez avoir deux arguments pour exécuter cette commande.";
fi

