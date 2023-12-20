from flask_redis import FlaskRedis, client

db: client = FlaskRedis()

# 初始化
# todo(jcz)
# db['fid'] = 1

# db.set('fid', 1)
# db.set('rid', 1)
# db.set('eid', 1)
# db.set('aid', 1)
