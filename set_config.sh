#!/bin/bash
# MAKE SURE YOU USE SOURCE ./set_config.sh
# Set environmental variable for out flask app
echo 'HEY BOZO! Did you make sure to run this using SOURCE?'
echo 'If so, carry on....'
echo '    '


echo What environment are you working in?
echo 1 - Development or 2 - Production
read env

if [ $env = 1 ]
then
  echo you are working in the Development environment
  export APPLICATION_SETTINGS='config.DevelopmentConfig'
else
  echo you are working in the Production environment
  export APPLICATION_SETTINGS='config.ProductionConfig'
fi

# flask will look for this but it only exists in production
#export HEROKU_POSTGRESQL_OLIVE_URL='nothingtoseehere'

