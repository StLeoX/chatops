import pytest
import app


# setup redis
@pytest.fixture
def redis():
    # setup
    app.create_app(debug=True)
    yield app.the_redis

    # teardown
    # 清空 0 数据库
    app.the_redis.flushdb()


# 模拟 `/gen_fault_desc` 接口对 redis 的使用
def test_redis_for_gen_fault_desc(redis):
    # mock
    redis.hset('faults', 1, "fault_a")
    rid, report, analysis = 1, "report_a", "analysis_a"

    # test
    fid = int(redis['fid'].decode())
    assert fid == 1
    fault = redis.hget('faults', fid).decode()
    assert fault == "fault_a"

    rid = redis.incr('rid')
    redis.hset('reports', rid, report)
    assert rid == 2
    assert redis.hget('reports', rid).decode() == 'report_a'

    aid = redis.incr('aid')
    assert aid == 2

    redis.incr('fid')
    assert int(redis['fid'].decode()) == 2


# 模拟 `/gen_fault_result` 接口对 redis 的使用
def test_redis_for_gen_fault_result(redis):
    # todo(fxc)
    pass
