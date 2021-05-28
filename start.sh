export QUIMBAYA_MYSQL_HOST='localhost'
export QUIMBAYA_MYSQL_USER='agudelo'
export QUIMBAYA_MYSQL_PWD='*FLDSmdfr*1200*'
export QUIMBAYA_MYSQL_DB='quimbaya'
export QUIMBAYA_TYPE_STORAGE='db'
export QUIMBAYA_SECRET_KEY='agudelo420a8bb13dc3bbc18768c7433db3c43b39e399e3b6ef1326bd4fe564e'
# export QUIMBAYA_ENV='test' # Warning: if the value is 'test', all data in the db will be deleted
uvicorn api.v1.main:app --host 0.0.0.0 --port 5000 --reload --header server:agudelo
