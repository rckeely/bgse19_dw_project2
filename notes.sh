
# General notes
# Nandan's deployment gist
# [ https://gist.github.com/nandanrao/a33618f54644b3d028f9f99b811f9f54 ]
# Tutorial on dash
# [ https://github.com/bgsedatascience/warehousing-dash-tutorial ]

# Switching to onclick handler
# [ https://plot.ly/python/click-events/ ]

# Connecting to Server
ssh -i "DWHW1.pem" ubuntu@ec2-52-207-180-159.compute-1.amazonaws.com

# Running dash on Server

cd ~/project/
git clone https://github.com/rckeely/bgse19_dw_project2.git
cd bgse19_dw_project2
# Install venv
sudo apt install python3-venv
# Create venv
python3 -m venv venv

source venv/bin/activate

# Install modules
pip install dash==1.6.1 dash-daq==0.3.1 pandas
pip install dash_bootstrap_components Image cvxpy

# Maybe
pip install ipywidgets

# Deploying with Dash and Electric Beanstalk
# Getting this error :
# NotAuthorizedError - Operation Denied. Access Denied
# Access key : [ AKIASLSWBBLUIEOZVQGV ]
# Secret Access key : [ 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 ]
