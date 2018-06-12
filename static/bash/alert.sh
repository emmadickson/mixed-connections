#!/usr/bin/env bash
( speaker-test -t sine -f 1000 )& pid=$! ; sleep .5s ; kill -9 $pid
