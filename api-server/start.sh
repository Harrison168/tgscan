#!/bin/bash

nohup java -jar -Dspring.profiles.active=prod api-server.jar > /dev/null 2>&1 &
