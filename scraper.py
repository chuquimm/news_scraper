import requests
import lxml.html as html
import os
import datetime

HOST = 'https://elcomercio.pe'
NEWS_PAGE = HOST+'/ultimas-noticias'
XPATH_LINKS = '//h2[@class="story-item__content-title overflow-hidden"]/a/@href'
XPATH_TITILE = '//h1[@class="sht__title"]/text()'
XPATH_SUMMARY = '//h2[@class="sht__summary"]/text()'
XPATH_BODY = '//div[@class="story-contents__content  false"]/section//*/text()'


def parse_notice(link, today):
    try:
        url = HOST + link
        response = requests.get(url)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITILE)[0]
                title = title.replace('\"', '')
                title = title.replace('\/', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError as e:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as e:
        print(e)


def parse_home():
    try:
        response = requests.get(NEWS_PAGE)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links = parsed.xpath(XPATH_LINKS)
            print('{} news'.format(len(links)))

            today = datetime.date.today().strftime('%Y-%m-%d')

            # create today folder
            if not os.path.isdir(today):
                os.mkdir(today)

            for i, link in enumerate(links):
                parse_notice(link, today)
                print('{}/{}'.format(i,len(links)))
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as e:
        print(e)


def run():
    parse_home()


if __name__ == "__main__":
    run()
