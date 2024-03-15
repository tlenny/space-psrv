import json
import urllib3

URL_OPS = 'http://ops.q7link.com:8080'

GQL_TENANTS = """
{
  Tenant(criteriaStr: "__criteria__ and clusterId is not null and startDate is not null", maxResult: 10) {
    id
    name
    clusterId
    enterpriseTypeId
  }
}
"""


def get_env_list():
    url = f'{URL_OPS}/api/qqsystem/busenv/?page=1&limit=999'
    data = get(url, {'Content-Type': 'application/json'})
    data = json.loads(data)
    print(data)
    result = []
    for env in data['data']:
        env_name = env['envName']
        if not env_name.startswith('nx-') and not env_name.endswith('-global'):
            result.append(env)
    return result
    # return mock_data('mockdata/q7/env.json')


def get_env_config(env_id):
    print(env_id)
    # return mock_data('mockdata/q7/env_config.json')
    url = f'{URL_OPS}/api/qqtools/serverinfo/?page=1&limit=20&env={env_id}'
    data = get(url, {'Content-Type': 'application/json'})
    data = json.loads(data)
    print(data)
    return data


def get_tenant_list(key, global_env, env_type):
    # return [{"id": "47L0LP505840001", "name": "cn-apnorthbj-1 | 47L0LP505840001 |财务/项目集群0-多组织 | 测试"},
    #         {"id": "C2M3BN505E80001", "name": "cn-northwest-1 | C2M3BN505E80001 | 北京企企科技有限公司 | 正式"}]
    domain = ''
    if env_type == 'prod':
        domain = '77hub.com'
    else:
        domain = 'e7link.com'
    url = f'http://identity.{global_env}.{domain}/identity/graphql/withoutAuth'
    keywords = key.split(' ')
    criteria = ''
    for keyword in keywords:
        if criteria != '':
            criteria += ' and '
        criteria += f"(id like '%{keyword}%' or name like '%{keyword}%')"

    gql = GQL_TENANTS.replace('__criteria__', criteria)
    print(gql)
    data = gql_query(url, gql, '0')
    data = data['Tenant']
    print(data)
    result = []
    for tenant in data:
        tenant_id = tenant['id']
        tenant_cluster_id = tenant['clusterId']
        tenant_name = tenant['name']
        tenant_type = '正式'
        if tenant['enterpriseTypeId'] == 'testingTenant':
            tenant_type = '测试'
        result.append({'id': tenant_id, 'name': f'{tenant_cluster_id} | {tenant_id} | {tenant_name} | {tenant_type}'})
    return result


def get(url, headers):
    http = urllib3.PoolManager()
    r = http.request(
        'GET',
        url,
        headers=headers
    )
    return r.data


def post(url, data, headers):
    http = urllib3.PoolManager()
    encoded_data = json.dumps(data).encode('utf-8')
    r = http.request(
        'POST',
        url,
        body=encoded_data,
        headers=headers
    )
    return r.data


def gql_query(url, gql, tenant_id):
    data = {'query': gql}
    headers = {'Content-Type': 'application/json', 'Tenant-Id': tenant_id}
    tenant_data = post(url, data, headers)
    print(tenant_data)
    json_data = json.loads(tenant_data)
    return json_data['data']


def post(url, data, headers):
    http = urllib3.PoolManager()
    encoded_data = json.dumps(data).encode('utf-8')
    r = http.request(
        'POST',
        url,
        body=encoded_data,
        headers=headers
    )
    return r.data


def mock_data(file_name):
    with open(file_name, 'r') as mock_file:
        md = json.load(mock_file)
        print(md)
        return md
