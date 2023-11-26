import requests, csv
from bs4 import BeautifulSoup
import re


url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu"


filename = "dc_data.csv"
f = open(filename, "a", encoding = "utf-8-sig", newline="")
writer = csv.writer(f)

columns_name = ["제목"]
writer.writerow(columns_name)


    # 웹서버에 요청
res = requests.get(url)
res.raise_for_status()

    # soup 인스턴스
soup = BeautifulSoup(res.text, "html.parser")
dataBox = soup.find_all("font", class_="list_title")

# 최근 게시글 번호 구하기
td_tag = soup.find("tr", class_=f'common-list1')
td_num = td_tag.find("td", class_='eng list_vspace')
td_num = td_num.get_text(strip=True)

for i in range(400000, int(td_num) + 1):
    url2 = f"https://www.ppomppu.co.kr/zboard/view.php?id=ppomppu&page=1&divpage=84&no={i}"
    res2 = requests.get(url2)
    res2.raise_for_status()
    soup2 = BeautifulSoup(res2.text, "html.parser")
    """
    og_title_tag = soup2.find("meta", property="og:title")
    if og_title_tag:
        og_title_content = og_title_tag.get("content")
        print("og:title 프로퍼티 값:", og_title_content)
    else:
        print("og:title 메타 태그를 찾을 수 없습니다.")
        """
    og_title_tag = soup2.find("span", class_="subject_preface type2")
    if og_title_tag:
        og_title_content = og_title_tag.text.strip()
        
        # Use regular expression to extract text inside square brackets
        match = re.search(r'\[(.*?)\]', og_title_content)
        
        if match:
            extracted_text = match.group(1)
            print(f"게시물 {i}의 제목: {extracted_text}")
        else:
            print(f"게시물 {i}의 제목에서 대괄호 안의 내용을 찾을 수 없습니다.")
    