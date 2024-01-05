import app

# Redis based model
class RedisModel:
    def __init__(self):
        self.redis = app.the_redis

    def save(self, key, data):
        self.redis.hset(self.__class__.__name__, str(key), str(data))
    
    def get(self, key):
        self.redis.hget(self.__class__.__name__, str(key))
    
    def delete(self, key):
        self.redis.hdel(self.__class__.__name__, str(key))

    def exists(self, key):
        self.redis.hexists(self.__class__.__name__, str(key))
    
    def get_all(self):
        return self.redis.hgetall(self.__class__.__name__)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.get_all()}>"

# 故障场景描述
class FaultDesc(RedisModel):
    def __init__(self,  fid):
        super().__init__()
        self.fid = fid
    
    def save(self, data):
        super().save(self.fid, data)
    
    def get(self):
        return super().get(self.fid)

    def delete(self):
        super().delete(self.fid)
    
    def exists(self):
        return super().exists(self.fid)

    def __repr__(self):
        return f"<FaultDesc {self.fid, self.get()}>"

# 用户期望描述
class Expectation(RedisModel):
    def __init__(self, eid):
        super().__init__()
        self.eid = eid
    
    def save(self, data):
        super().save(self.eid, data)
    
    def get(self):
        return super().get(self.eid)
    
    def delete(self):
        super().delete(self.eid)
    
    def exists(self):
        return super().exists(self.eid)
    
    def __repr__(self):
        return f"<Expectation {self.eid, self.get()}>"

# 生成运维建议
class FaultReport(RedisModel):
    def __init__(self, rid):
        super().__init__()
        self.rid = rid
    
    def save(self, data):
        super().save(self.rid, data)
    
    def get(self):
        return super().get(self.rid)
    
    def delete(self):
        super().delete(self.rid)
    
    def exists(self):
        return super().exists(self.rid)
    
    def __repr__(self):
        return f"<FaultReport {self.rid, self.get()}>"
    
