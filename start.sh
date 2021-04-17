export QUIMBAYA_MYSQL_HOST='localhost'
export QUIMBAYA_MYSQL_USER='agudelo'
export QUIMBAYA_MYSQL_PWD='PROTECTED-DATA'
export QUIMBAYA_MYSQL_DB='quimbaya'
export QUIMBAYA_TYPE_STORAGE='db'
# export QUIMBAYA_ENV='test' # Warning: if the value is 'test', all data in the db will be deleted
uvicorn api.v1.main:app --host 0.0.0.0 --port 5000 --reload --header server:agudelo
