from operator import itemgetter
import xml.etree.ElementTree as XML
import csv
import json
import requests
from xmljson import yahoo


def nome_tratado(name: str) -> str:
    new_name = name.lower().replace(' ', '-')
    return new_name


def get_plataform_id(name: str) -> list:
    js = []
    link = 'http://thegamesdb.net/api/GetPlatformsList.php'
    nome = nome_tratado(name)
    get_xml = requests.get(link)
    xml = XML.fromstring(get_xml.text)

    for plataforms in xml[1]:
        if plataforms[2].text.find(nome) == 0:
            js.append({
                'id': plataforms[0].text,
                'fullname': plataforms[1].text,
                'name': plataforms[2].text
            })
    return js


def get_games_plataform(id: int):
    link = 'http://thegamesdb.net/api/GetPlatformGames.php?platform={}'
    get_xml = requests.get(link.format(id))
    xml = XML.fromstring(get_xml.text)
    rows = []

    for game in xml:
        rows.append({
            'id': game[0].text,
            'name': game[1].text,
        })

    return sorted(rows, key=itemgetter('Nome'))


def write_games_plataform_csv(id: int):
    header = ['id', 'name']
    with open('jogos.csv', 'w+') as csvfile:
        file = csv.DictWriter(csvfile, header)
        file.writeheader()
        file.writerows(get_games_plataform(id))


def game_detail(id: int, platform: int):
    link = 'http://thegamesdb.net/api/GetGame.php?id={}&platform={}'.format(
        id, platform)

    request = requests.get(link)
    xml_to_dict = yahoo.data(XML.fromstring(request.content))
    return xml_to_dict


if __name__ == '__main__':
    # ids = get_plataform_id('sony')
    # print(json.dumps(ids, indent=4))

    # for id in ids:
        # print(id['name_title'])

    # write_games_plataform_csv(11)

    game_detail(id=15, platform=11)
