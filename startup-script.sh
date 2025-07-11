#!/bin/bash
apt update
apt install -y python3-pip git
pip3 install flask mysql-connector-python

# Clone repo
git clone https://github.com/Praveenarumugam07/employee-app.git
cd employee-app

# Install requirements
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
fi

# Modify app.py to run on port 80
sed -i 's/app.run(/app.run(host="0.0.0.0", port=80, /' app.py

# Run app on port 80
nohup python3 app.py &
