import pytest
from sample_pkg.sample import Sample


@pytest.fixture(scope='function')
def mocker_post_tasks(mocker):
    return mocker.patch('sample_pkg.sample.post_tasks')


@pytest.fixture(scope='function')
def mocker_wait_wf(mocker):
    return mocker.patch('sample_pkg.sample.wait_wf')


@pytest.mark.unittest
def test_with_mock(mocker_post_tasks, mocker_wait_wf):
    mocker_post_tasks.return_value = {"workflow_id": 'wf-123'}
    mocker_wait_wf.return_value = {"workflow_id": 'wf-123', 'status': 'SUCCEEDED'}

    status = Sample.run_something_on_cyto_cc(input1='bla', input2='foo-foo')

    mocker_wait_wf.assert_called_with('wf-123', wait_for_descendants=True, interval=69)
    assert status == 'SUCCEEDED'
