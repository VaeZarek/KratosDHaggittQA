#!/usr/bin/env bash
# Bash Script to ping a set of IPs:
# 192.168.1.1 to 192.168.1.254

# Prefix of IP addresses
PREFIX=$'192.168.1.';

# Ping 1-254, appending SUFFIX
for SUFFIX in {1..254}
do
  # Perform ping in background to be efficient
  ping -c 1 -q $PREFIX$SUFFIX 2>&1 &

  # Sleep to make sure output comes out in order
  sleep 0.01
done

# Wait until all ping jobs are done
wait
