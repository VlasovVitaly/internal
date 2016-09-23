#!/usr/bin/env python3

import sys
import pickle
import urllib.parse
import urllib.request
try:
    import lxml.html as lhtml
except ImportError:
    print("lxml module is required. Install it")
    sys.exit(1)


server_url = 'http://gatherer.wizards.com/'
base_url =  server_url + 'Pages/'
search_url = base_url + 'Search/'
search_page_url = search_url + 'Default.aspx'


def _parse_img_cost(img_tag):
    alt = img_tag.get('alt')
    try:
        int(alt)
        return '{' + alt + '}'
    except ValueError:
        pass

    if alt == 'Tap':
        return '{T}'
    elif alt == 'Red':
        return '{R}'
    elif alt == 'Black':
        return '{B}'
    elif alt == 'White':
        return '{W}'
    elif alt == 'Green':
        return '{G}'
    elif alt == 'Blue':
        return '{I}'
    elif alt == 'Variable Colorless':
        return '{X}'
    elif alt == 'Colorless':
        return '{CL}'
    else:
        print("UNKNOWN MANA COST")
        sys.exit(0)
        return '{UNKNOWN}'

def _parse_text_with_tags(elt):
    children = elt.getchildren()
    if len(children) == 0:
        return elt.text_content()

    part = elt.text or ''
    for child in children:
        if len(child.getchildren()) != 0:
            part +=  _parse_text_with_tags(child)
            continue
        if child.tag == 'img':
            part += _parse_img_cost(child)
        else:
            part += child.text
        if child.tail:
            part += child.tail
    if elt.tail:
        part += elt.tail

    return part

def parse_card_from_url(url):
    card_data = {}

    with urllib.request.urlopen(url) as response:
        html_doc = lhtml.fromstring(response.read())

    root_elt = html_doc.find_class('cardDetails')
    if root_elt:
        root_elt = root_elt[0]
    else:
        print("Can't find card detail table")
        return

    left_col = root_elt.find_class('leftCol')
    if left_col:
        left_col = left_col[0]
    else:
        print("Can't find card detail left column")
        return

    right_col = root_elt.find_class('rightCol')
    if right_col:
        right_col = right_col[0]
    else:
        print("Can't find card detail rigth column")
        return

    # Image
    img_div = left_col.find_class('cardImage')
    if img_div:
        img_div = img_div[0]
    else:
        print("Can't find card image link")
        return
    img_div.make_links_absolute(url)
    for l in img_div.iterlinks():
        card_data['img_link'] = l[2]

    # Card name
    cname = right_col.get_element_by_id("ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow")
    if cname == None:
        print("Can't find card name")
        return
    cname = cname.find_class('value')[0]
    text = str(cname.text_content()).replace('\\r\\n', '').strip()
    card_data['name'] = text

    # Mana cost
    try:
        mana_cost = right_col.get_element_by_id("ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow")
    except KeyError:
        card_data['mana_cost'] = []
    else:
        mana_cost = mana_cost.find_class("value")[0]
        card_data['mana_cost'] = []
        for img in mana_cost:
            card_data['mana_cost'].append(_parse_img_cost(img))

    # Converted mana cast
    try:
        cmc = right_col.get_element_by_id("ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow")
    except KeyError:
        card_data['cmc'] = None
    else:
        cmc = cmc.find_class('value')[0]
        text = str(cmc.text_content()).replace('\\r\\n', '').strip()
        try:
            card_data['cmc'] = int(text)
        except:
            print("Can't convert cmc value in to integer")
            return

    # Card type
    ctype = right_col.get_element_by_id("ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow")
    if ctype == None:
        print("Can't find card type")
        return
    ctype = ctype.find_class('value')[0]
    text = str(ctype.text_content()).replace('\\r\\n', '').strip()
    text = text.replace('\\xe2\\x80\\x94', '—')
    card_data['card_type'] = text

    # Card Text
    try:
        ctext = right_col.get_element_by_id("ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow")
    except KeyError:
        card_data['text'] = []
    else:
        ctext = ctext.find_class('value')[0]
        ctext_list = []
        for p in ctext.find_class('cardtextbox'):
            ctext_list.append(_parse_text_with_tags(p))
        card_data['text'] = ctext_list

    # Card set
    cset = right_col.get_element_by_id("ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_setRow")
    if cset == None:
        print("Can't get card expansion")
        return
    cset = cset.find_class('value')[0][0]
    card_data['set'] = str(cset[1].text_content())

    # Rarity
    crarity = right_col.get_element_by_id("ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow")
    if crarity == None:
        print("Can't get card rarity")
        return
    crarity = crarity.find_class('value')[0]
    text = str(crarity.text_content()).replace('\\r\\n', '').strip()
    card_data['rarity'] = text

    # Card number
    cnum = right_col.get_element_by_id("ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberRow")
    if cnum == None:
        print("Can't get card number")
        return
    cnum = cnum.find_class('value')[0]
    text = str(cnum.text_content()).replace('\\r\\n', '').strip()
    try:
        card_data['number'] = int(text)
    except:
        print("Can't convert number value in to integer")
        return

    # Artist
    cartist = right_col.get_element_by_id("ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ArtistCredit")
    if cartist == None:
        print("Can't get card artist")
        return
    card_data['artist'] = str(cartist[0].text_content())

    # Power Toughness
    try:
        cpt = right_col.get_element_by_id("ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow")
    except KeyError:
        card_data['power'] = None
        card_data['toughness'] = None
    else:
        test_label = cpt.find_class('label')[0]
        test_label = test_label.text_content().replace('\\r\\n', '').strip()
        cpt = cpt.find_class('value')[0]
        pt = str(cpt.text_content()).replace('\\r\\n', '').strip()
        if test_label == 'Loyalty:':
            card_data['power'] = None
            card_data['toughness'] = None
            card_data['loyalty'] = pt.strip()
        else:
            pt = pt.split('/')
            card_data['power'] = pt[0].strip()
            card_data['toughness'] = pt[1].strip()

    # Flavor Text
    try:
        flavor = right_col.get_element_by_id("ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_FlavorText")
    except KeyError:
        card_data['flavor_text'] = []
    else:
        flavor_text = []
        for p in flavor:
            flavor_text.append(str(p.text_content()).replace('\\xe2\\x80\\x94', '—'))
        card_data['flavor_text'] = flavor_text

    return card_data

def get_page_cards(elts):
    links = []
    for e in elts:
        e.make_links_absolute(search_url)
        for l in e.iterlinks():
            links.append(l[2])

    return links

def get_cards_list(url, set_name, page):
    query = { 'action': 'advanced', 'page': str(page) }
    query['set'] = '["{}"]'.format(set_name)

    url = url + '?' + urllib.parse.urlencode(query)

    with urllib.request.urlopen(url) as response:
        html_doc = lhtml.fromstring(response.read())

    table = html_doc.find_class('cardItemTable')[0]
    card_links = get_page_cards(table.find_class('cardTitle'))

    return card_links

def parse_set_url(base_url, set_name, output_file):
    query = { 'action': 'advanced' }
    query['set'] = '["{}"]'.format(set_name)

    url = base_url + '?' + urllib.parse.urlencode(query)

    print("Parsing set: {}".format(set_name))
    print("Url: {}".format(url))

    with urllib.request.urlopen(url) as response:
        html_doc = lhtml.fromstring(response.read())

    cards = []
    table = html_doc.find_class('cardItemTable')[0]
    card_links = get_page_cards(table.find_class('cardTitle'))

    paging_block = html_doc.find_class('paging')
    if len(paging_block):
        paging_root = paging_block[0]
        # Need to find last page number
        next_link = paging_root.xpath('.//a[text()=" >"]')
        last_link = paging_root.xpath('.//a[text()=">>"]')
        if not last_link:
            last_link = next_link[0].xpath('./preceding-sibling::a')[-1]
        parsed_url = urllib.parse.urlparse(last_link.attrib['href'])
        last_page = urllib.parse.parse_qs(parsed_url.query)['page'][0]

        # Allready parsed page #0 so start from 1
        for page_num in range(1, int(last_page) + 1):
            print("Getting cards links from page {}".format(page_num))
            card_links = card_links + get_cards_list(base_url, set_name, page_num)

    total_cards = len(card_links)
    print("Set contain {} cards links".format(total_cards))
    for num,link in enumerate(card_links, start=1):
        print("Parsing card {} of {}: {}".format(num, total_cards, link))
        card = parse_card_from_url(link)
        if card:
            print(card)
            print("---")
            cards.append(card)
        else:
            print("Something wrong with card on link: {}".format(link))
            return
    print("Totaly parsed {} cards.".format(total_cards))

    print("Saving to pickle file.")
    with open(output_file, "wb") as output:
        pickle.dump(cards, output, pickle.HIGHEST_PROTOCOL)
        print("Pickle data file was saved.")

def load_from_pickle(fname):
    with open(fname, "rb") as ifile:
        data = pickle.load(ifile)
    return data or ()

def pprint_cards(cards):
    for card in cards:
        print("Name: {}".format(card['name']))
        print("Mana cost: {}".format(''.join(card['mana_cost']) or  None))
        print("Converted mana cost: {}".format(card['cmc']))
        print("Type: {}".format(card['card_type']))
        print("Expansion: {}".format(card['set']))
        print("Rarity: {}".format(card['rarity']))
        if card.get('loyalty'):
            print("Loyalty: {}".format(card['loyalty']))
        else:
            print("Power: {}".format(card.get('power')))
            print("Toughness: {}".format(card.get('toughness')))
        if card['text']:
            print("Card text:")
            for t in card['text']:
                print("   {}".format(t))
        else:
            print("Card text: None")
        if card['flavor_text']:
            print("Flavor text:")
            for t in card['flavor_text']:
                print("   {}".format(t))
        else:
            print("Favor text: None")
        print("Number: {}".format(card['number']))
        print("Artist: {}".format(card['artist']))
        print("Picture link: {}".format(card['img_link']))
        print("-" * 10)

if __name__ == '__main__':
    try:
        import argparse
    except ImportError as err:
        print(err)
        sys.exit(1)
    parser = argparse.ArgumentParser(
        prog="parse-gatherer",
        description="Parser of MTG Gatherer site."
    )

    subparsers = parser.add_subparsers(
        title="Mode",
        metavar="<mode>",
        dest="mode"
    )
    subparsers.required = True

    read_sub = subparsers.add_parser(
        "load",
        help="Load and print data from pickled file."
    )
    read_sub.add_argument(
        "input_filename",
        metavar="INPUTFILE",
        help="Input file name"
    )

    write_sub = subparsers.add_parser(
        "parse",
        help="Parse expansion set and store it in pickle file"
    )
    write_sub.add_argument(
        "set_name",
        metavar="SET NAME",
        help="Name of expansion set"
    )
    write_sub.add_argument(
        "output_filename",
        metavar="OUTPUTFILE",
        help="Output file name"
    )
    test_sub = subparsers.add_parser(
        "testurl",
        help="Test card url"
    )
    test_sub.add_argument(
        "url",
        metavar="URL",
        help="Gatherer card url"
    )
    args = dict(vars(parser.parse_args()))
    if args['mode'] == 'load':
        cards = load_from_pickle(args['input_filename'])
        pprint_cards(cards)
    elif args['mode'] == 'parse':
        parse_set_url(search_page_url, args['set_name'], args['output_filename'])
    elif args['mode'] == 'testurl':
        ret = parse_card_from_url(args['url'])
        print(ret or "Can't parse card from {}".format(args['url']))
    sys.exit(0)
