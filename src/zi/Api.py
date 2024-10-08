from fastapi import APIRouter
import requests
from bs4 import BeautifulSoup
import json


router = APIRouter(
    prefix="/dict",
    tags=["dict"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/zi")
async def get(wd):
    url = 'http://www.ccamc.co/cjkv.php?cjkv=' + wd
    response = requests.get(url)

    result = []

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')

        result_map = {}

        # 查找指定的 div 元素
        for div in soup.find_all('div', {"class": "zy"}):
            # 查找下级的 span 元素
            for span in div.find_all('span'):
                key = span.get('class')[0]  # 获取 class 名称作为键
                value = span.text.strip()  # 获取文本内容作为值
                result_map[key] = value  # 添加到字典中

        # 打印结果
        print(result_map)
        url_post = 'http://www.ccamc.co/components/CJKV/get_ziyi_new.php'
        post_response = requests.post(url_post, data=result_map)

        # 检查 POST 请求是否成功
        if post_response.status_code == 200:
            # print("POST 请求成功，返回内容：", post_response.text)

            # 解析 HTML 内容
            post_soup = BeautifulSoup(post_response.text, 'html.parser')

            html_content = post_soup.prettify()
            print(html_content)
            # 查找指定的 div 元素
            for div in post_soup.find_all('div', {"class": "row main"}):
                # 查找下级的 span 元素
                h3 = div.find_next('h3')
                item = {}
                result.append(item)
                item['title'] = h3.text.strip()
                # sub_div = div.find_all('div', {"class": "hydzd"})
                p_list = div.find_all('p')
                arr = []
                html_arr = []
                for p in p_list:
                    # 移除 div 中的所有 <a> 标签
                    for a_tag in p.find_all('a'):
                        a_tag.decompose()  # 完全移除 <a> 标签及其内容
                    html_arr.append(p.prettify())
                    arr.append(p.text.strip())

                item['content'] = arr
                item['html'] = html_arr

            # 打印结果
            print(json.dumps(result, indent=4, ensure_ascii=False))

        else:
            print(f"POST 请求失败，状态码: {post_response.status_code}")
    else:
        print(f"请求失败，状态码: {response.status_code}")
    return result



