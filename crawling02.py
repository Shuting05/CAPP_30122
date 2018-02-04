import bs4
import urllib3
import csv
import string
import re



def write_csv():
    '''
    search key words in grad cafe website and call crawler to write a csv file
    '''
    key_words = string.ascii_lowercase

    with open('all_cases.csv', 'w', newline='') as csvfile:
        cases = csv.writer(csvfile, delimiter=',')
        row = (['case_id', 'institute', 'program', 'degree', 'season', \
            'decision', 'notification', 'result_date', 'undergrad gpa', \
            'gre_v', 'gre_q', 'gre_w', 'gre_subject', 'status', 'submit_date', 'notes'])
        cases.writerow(row)
        case_id_set = set()
        for i in key_words:
            crawler(i, cases, case_id_set)


def crawler(key_word, csv_writer, case_id):
    '''
    crawl the webpages with key_word, strip attributes and write them \
    into the csv file

    inputs:
    key_word: the key word to search
    csv_writer: a csv writer
    case_id: a set containing cases' ids that have been written

    '''

    origin_url = 'http://thegradcafe.com/survey/index.php?q={}%2A&t=a&pp=250&o=&p=1'.format(key_word)
    page_num = find_n_pages(origin_url)

    for i in range(1, page_num+1):
        url = 'http://thegradcafe.com/survey/index.php?q={}%2A&t=a&pp=250&o=&p={}'.format(key_word, i)
        pm = urllib3.PoolManager()
        html = pm.urlopen(url=url, method="GET").data
        soup = bs4.BeautifulSoup(html, "html5lib")
        table_list = soup.find_all("table")
        table = table_list[0]
        tr_list = table.find_all("tr")[1:]


        for tr in tr_list:
            # column 1
            id_string = tr['onmouseover']
            tr_id = int(re.findall('\d+', id_string)[0])
            if tr_id not in case_id:
                (institute, program, degree, season, decision,notification,\
                 result_date, gpa, gre_v, gre_q, gre_w, gre_subject, status,\
                  submit_date, notes) = tuple([None]*15)
                case_id |= {tr_id}
                td_list = tr.find_all("td")
                # column 2
                institute = td_list[0].text

                pro_deg_sea = td_list[1].text
                # column 3
                program = ', '.join(pro_deg_sea.split(',')[:-1])
                # column 4
                if len(re.findall(', \w+', pro_deg_sea)) >= 1:
                    degree = re.findall(', \w+', pro_deg_sea)[-1][2:]

                # column 5
                season = ''
                if re.findall('[a-zA-Z]\d\d', pro_deg_sea):
                    season = re.findall('[a-zA-Z]\d\d', pro_deg_sea)[0]
                # column 6

                span = td_list[2].find_all('span')
                if span:
                    if span[0].has_attr('class'):
                        decision = span[0].text

                dds = td_list[2].text
                # column 7
                if re.findall('via\s\w+', dds):
                    notification = re.findall('via\s\w+', dds)[0]
                # column 8

                if re.findall('\d\d? [A-Z][a-z]* \d{4}',dds):
                    result_date = re.findall('\d\d? [A-Z][a-z]* \d{4}',dds)[0]

                if td_list[2].find_all('a'):
                    gpa_score = td_list[2].find_all('a')[0]
                    # column 9
                    gpa = gpa_score.find_all('strong')[0].next_sibling[2:]
                    gre_general = tuple(gpa_score.find_all('strong')[1].next_sibling[2:].split('/'))
                    # column 10,11,12
                    gre_v, gre_q, gre_w = tuple(map(float, gre_general))
                    # column 13
                    gre_subject = (gpa_score.find_all('strong')[2].\
                                                            next_sibling[2:])
                # column 14
                status = td_list[3].text
                # column 15
                submit_date = td_list[4].text
                # column 16
                notes = td_list[5].text

                row = ([tr_id, institute, program, degree, season, decision,\
                    notification, result_date, gpa, gre_v, gre_q, gre_w, \
                    gre_subject, status, submit_date, notes])

                csv_writer.writerow(row)

def find_n_pages(origin_url):
    '''
    input:
    origin_url(string): the origin url for a key word

    return:
    page_num(integer): number of pages found with the key word
    '''
    pm = urllib3.PoolManager()
    html = pm.urlopen(url=origin_url, method="GET").data
    soup = bs4.BeautifulSoup(html, "html5lib")
    text = soup.find_all("div", class_="pagination")[0].text
    page_num = int(re.findall("\d+ pages", text)[0][:-6])

    return page_num
