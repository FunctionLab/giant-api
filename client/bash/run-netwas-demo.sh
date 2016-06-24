#!/bin/bash

printf "$0 started\n\n"

printf "1. Create new NetWAS job\n\n"
cmd='curl -s http://giant-api.princeton.edu/netwas/jobs 
                 -F gwas_file=@bmi-2012.txt 
                 -F gwas_format=vegas 
                 -F tissue=api-demo 
                 -F p_value=0.01 
                 -F title="NetWAS from shell script" | python -m json.tool'
printf "   command: $cmd\n\n"
result=$(eval $cmd)
printf "   result: $result"
printf "\n\n"

printf "2. Submit NetWAS job to GIANT server and start SVM training\n\n"
id=$(printf "$result" | grep '"id": ' | tr -d ' ' | cut -d'"' -f4)
cmd="curl -s -X POST http://giant-api.princeton.edu/netwas/jobs/$id/start | python -m json.tool"
printf "   command: $cmd\n\n"
result=$(eval $cmd)
printf "   result: $result"
printf "\n\n"

printf "3. Wait 15 s for NetWAS job to start executing on GIANT server\n"
printf "   "
for i in `seq 1 15`;
do
	sleep 1
	printf "."
done
printf "\n"
printf "   Print current job status (expected status: 'running')\n\n"
cmd="curl -s http://giant-api.princeton.edu/netwas/jobs/$id | python -m json.tool"
printf "   command: $cmd\n\n"
result=$(eval $cmd)
printf "   result: $result"
printf "\n\n"

printf "4. Print training log (first 10 lines)\n\n"
log=$(printf "$result" | grep '"log_file": ' | tr -d ' ' | cut -d'"' -f4)
cmd="curl -s $log | head"
printf "   command: $cmd\n\n"
result=$(eval $cmd)
printf "   log:\n>>>\n"
printf "$result"
printf "\n...\n<<<\n\n"

printf "5. Wait 30 s for NetWAS job to complete on GIANT server\n"
printf "   "
for i in `seq 1 30`;
do
	sleep 1
	printf "."
done
printf "\n"
printf "   Print current job status (expected status: 'completed')\n\n"
cmd="curl -s http://giant-api.princeton.edu/netwas/jobs/$id | python -m json.tool"
printf "   command: $cmd\n\n"
result=$(eval $cmd)
printf "   result: $result"
printf "\n\n"

printf "6. Print training log (last 10 lines)\n\n"
rf=$(printf "$result" | grep '"results_file": ' | tr -d ' ' | cut -d'"' -f4)
cmd="curl -s $log | tail"
printf "   command: $cmd\n\n"
result=$(eval $cmd)
printf "   log:\n>>>\n...\n"
printf "$result"
printf "\n<<<\n\n"

printf "7. Print NetWAS output (first and last 10 lines)\n\n"
cmd="curl -s $rf"
printf "   command: $cmd\n\n"
result=$(eval $cmd | head)
printf "   netwas_output:\n>>>\n"
printf "$result"
printf "\n...\n"
result=$(eval $cmd | tail)
printf "$result"
printf "\n<<<\n\n"

printf "$0 completed\n"
