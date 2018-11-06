import pytest

class TestApp:

    @pytest.mark.util
    def test_get_ping(self, client):
        res = client.get('/ping')
        assert res.status_code == 200
        assert res.json == {'ping': 'pong'}

    @pytest.mark.util
    def test_get_healthz(self, client):
        res = client.get('/healthz')
        assert res.status_code == 200
        assert res.json == {'status':'SUCCESS'}

    @pytest.mark.get_request
    def test_get_tasks(self, client):
        res = client.get('/tasks')
        assert res.status_code == 200

    @pytest.mark.get_request
    @pytest.mark.parametrize("test_input,expected_output",[('/tasks/1',200),('/tasks/2',200),('/tasks/3',200),('/tasks/4',404)])
    def test_get_task_by_id(self,client,test_input,expected_output):
        res = client.get(test_input)
        assert res.status_code == expected_output
        #assert res.json['task']['done'] == False

    task_5 = dict(title='Get Paid',description='Complete Course')
    task_6 = dict(title='Get laid',description='Complete Course')
    task_7 = dict(title='She Said',description='Complete Course')

    @pytest.mark.post_request
    @pytest.mark.parametrize("test_endpoint,test_data,expected_output",[('/tasks',task_5,200),('/tasks',task_6,200),('/tasks',task_7,200)])
    def test_post_add_task(self,client,test_endpoint,test_data,expected_output):
        res = client.post(test_endpoint,data=test_data)
        assert res.status_code == expected_output

    @pytest.mark.delete_request
    @pytest.mark.parametrize("test_endpoint,expected_output",[('/tasks/1',200),('/tasks/2',200),('/tasks/3',200)])
    def test_delete_task(self,client,test_endpoint,expected_output):
        res = client.delete(test_endpoint)
        assert res.status_code == expected_output
