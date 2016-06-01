#!/bin/bash

printf "$0 started\n\n"

printf "1. Validate brain tissue\n"
cmd='curl giant-api.princeton.edu/tissues/check/brain'
printf "   command: $cmd\n"
printf "   result:  "
$cmd
printf "\n\n"

printf "2. Validate query genes\n"
cmd='curl giant-api.princeton.edu/genes/check/snca+park7'
printf "   command: $cmd\n"
printf "   result:  "
$cmd
printf "\n\n"

printf "3. Query functional network\n"
cmd='curl giant-api.princeton.edu/networks -s -d tissue=brain -d genes=SNCA+PARK7 | python -m json.tool 2> /dev/null | head -15'
printf "   command: $cmd\n"
printf "   result (first 15 lines):\n"
eval $cmd
printf "...\n\n"

printf "4. Query with different prediction parameters\n"
cmd='curl giant-api.princeton.edu/networks -s -d tissue=brain -d genes=SNCA+PARK7 -d num_genes=20 -d prior=0.15 | python -m json.tool 2> /dev/null | head -15'
printf "   command: $cmd\n"
printf "   result (first 15 lines):\n"
eval $cmd
printf "...\n\n"

printf "5. Query datasets supporting a specified gene interaction\n"
cmd='curl giant-api.princeton.edu/networks/evidence -s -d tissue=brain -d source=ATP5J -d target=PARK7 | python -m json.tool 2> /dev/null | head -15'
printf "   command: $cmd\n"
printf "   result (first 15 lines):\n"
eval $cmd
printf "...\n\n"

printf "$0 completed\n"
