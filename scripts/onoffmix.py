# encoding: utf-8

import requests
import sys

from bs4 import BeautifulSoup

EVENT_ID = 83852
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1)',
}

session = requests.Session()


def login(email, password):
    url = 'https://onoffmix.com:443/account/login'
    data = {
        'proc': 'login',
        'email': email,
        'pw': password,
    }
    r = session.post(url, data=data, headers=HEADERS)
    if r.text != '<script>location.href="http://onoffmix.com";</script>':
        print r.text
        print r.status_code
        exit(1)


def create_content(image_url):
    return \
        '<p>아래 이미지를 클릭하면 상세 페이지로 이동합니다.</p>'\
        '<p><a href="https://stac.github.io/staccato/" target="_blank">'\
        '<img src="{}"></a></p>'.format(image_url)


def upload_image(filename):
    url = 'http://onoffmix.com/_/file/upload.ofm'
    f = open(filename, 'rb')
    data = {
        'groupName': 'eventSkin',
        'postproc': 1,
    }
    files = {
        'Filedata': (filename, f, 'image/png'),
    }
    r = session.post(url, files=files, data=data, headers=HEADERS)
    if r.status_code == 200:
        values = r.text.split('|')
        url = values[4]
        return url
    else:
        print r.text
        print r.status_code
        exit(1)


def get_input_value(html, name):
    return html.find('input', {'name': name}).get('value')


def get_textarea_value(html, name):
    return html.find('textarea', {'name': name}).text


def get_select_value(html, name):
    return html.find('select', {'name': name}).get('data-value')


def get_base_data():
    url = 'http://onoffmix.com/event/{}/manage/edit/'.format(EVENT_ID)
    r = session.get(url, headers=HEADERS)
    html = BeautifulSoup(r.text, 'html.parser')
    event_start_datetime = get_input_value(html, 'eventStartDateTime')
    event_end_datetime = get_input_value(html, 'eventEndDateTime')
    recruit_start_datetime = get_input_value(html, 'recruitStartDateTime')
    recruit_end_datetime = get_input_value(html, 'recruitEndDateTime')
    abstract = get_textarea_value(html, 'abstract')
    owner_phone_head = get_select_value(html, 'ownerPhone_head')
    owner_phone_body = get_input_value(html, 'ownerPhone_body')
    owner_phone_tail = get_input_value(html, 'ownerPhone_tail')
    owner_email = get_input_value(html, 'ownerEmail')
    data = {
        'proc': 'modifyBaseEvent',
        'eventIdx': EVENT_ID,
        'eventEndDateInUse': 'y',
        'eventStartDateTime_date': event_start_datetime.split(' ')[0],
        'eventStartDateTime_time': event_start_datetime.split(' ')[1],
        'eventEndDateTime_date': event_end_datetime.split(' ')[0],
        'eventEndDateTime_time': event_end_datetime.split(' ')[1],
        'recruitStartDateInUse': 'y',
        'recruitStartDateTime_date': recruit_start_datetime.split(' ')[0],
        'recruitStartDateTime_time': recruit_start_datetime.split(' ')[1],
        'recruitEndDateTime_date': recruit_end_datetime.split(' ')[0],
        'recruitEndDateTime_time': recruit_end_datetime.split(' ')[1],
        'abstract': abstract,
        'content': '',
        'ownerPhone_head': owner_phone_head,
        'ownerPhone_body': owner_phone_body,
        'ownerPhone_tail': owner_phone_tail,
        'ownerEmail': owner_email,
    }
    return data


def edit(content):
    url = 'http://onoffmix.com/event/{}/manage/edit/'.format(EVENT_ID)
    data = get_base_data()
    data['content'] = content
    r = session.post(url, data=data, headers=HEADERS)
    print r.status_code


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: onoffmix.py email password image_filename'
        exit(1)
    (_, email, password, image_filename) = sys.argv
    login(email, password)
    image_url = upload_image(image_filename)
    content = create_content(image_url)
    edit(content)
