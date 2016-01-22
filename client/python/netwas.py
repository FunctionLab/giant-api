#!/usr/bin/env python

import datetime
import sys
import time

# Import NetWAS from GIANT API
from giantapi import NetwasJob

# Optionally specify an email that will receive notification of job results
# upon completion.
EMAIL = ''

# Begin demo
print "Started {0} at {1}.\n".format(sys.argv[0], datetime.datetime.now())
print ("This script uses the GIANT API to run a NetWAS job in demo mode,\n"
       "which is invoked by the setting \"tissue=api-demo\". This simulates a\n"
       "short SVM training, which completes in under 2 minutes. In order to\n"
       "run NetWAS on actual tissues, please replace \"api-demo\" with one of\n"
       "the 144 tissue choices supported by the API. Valid options are listed\n"
       "at http://giant-api.princeton.edu/tissues. Note that non-demo NetWAS\n"
       "tasks may take up to 30 minutes to complete.\n")

# Step 1
print "Step 1: Create new NetWAS job.."
nj1 = NetwasJob(title="GIANT API NetWAS Example in Python",
                gwas_file="./bmi-2012.out",
                gwas_format="vegas",
                tissue="api-demo",
                p_value=0.01,
                email=EMAIL)
print "\tDone. Job details (prior to submission to GIANT server):\n>>>"
print nj1, "\n<<<\n"
time.sleep(1)

# Step 2
print "Step 2: Submit NetWAS job to GIANT server and start SVM training.."
nj1.start()
print "\tDone. Updated job status:\n>>>"
print nj1, "\n<<<\n"
time.sleep(1)

# Step 3
print "Step 3: Wait 15 s for NetWAS job to start executing on GIANT server..\n\t",
for i in range(5):
    sys.stdout.write('.')
    time.sleep(3)
print "\n\tDone. Updated job status:\n>>>"
print nj1, "\n<<<"
print "\tCurrent training log:\n>>>"
print nj1.log(),
print "...\n<<<\n"

# Step 4
print "Step 4: Wait 30 s for NetWAS job to complete on GIANT server..\n\t",
for i in range(10):
    sys.stdout.write('.')
    time.sleep(3)
print "\n\tDone. Final job status:\n>>>"
print nj1, "\n<<<"
print "\tFinal training log:\n>>>"
print nj1.log(),
print "<<<"
print "\tJob results (first 15 rows):\n>>>"
results = nj1.results()
print "\n".join(results.splitlines()[0:15])
print "...\n<<<\n"

# End demo
print ("Job status and results are also accessible from the web interface of\n"
       "the API. Please visit:\n")
print "\thttp://giant-api.princeton.edu/netwas/jobs/{0}".format(nj1.id)
print "\nCompleted {0} at {1}.".format(sys.argv[0], datetime.datetime.now())
