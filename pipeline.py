import logging
logging.basicConfig(level=logging.INFO)
import subprocess
import datetime


logger = logging.getLogger(__name__)
news_site_uids = ['eluniversal', 'pagina12']


def main():
    _extract()
    _transform()
    _load()


def _extract():
    logger.info('Starting extract process')
    for news_site_uid in news_site_uids:
        subprocess.run(['python', 'main.py', news_site_uid], cwd='.//extract')
        subprocess.run(['find', '.', '-name', '{}*'.format(news_site_uid),
                        '-exec', 'mv', '{}', '..//transform//{}_.csv'.format(news_site_uid),
                        ';'], cwd='./extract')


def _transform():
    logger.info('Starting transform process')
    for news_site_uid in news_site_uids:
        dirty_data_filename = '{}_.csv'.format(news_site_uid)
        clean_data_filename = 'clean_{}'.format(dirty_data_filename)
        subprocess.run(['python', 'newspaper_recipe.py', dirty_data_filename], cwd='.//transform')
        subprocess.run(['rm', dirty_data_filename], cwd='.//transform')
        subprocess.run(['mv', clean_data_filename, '../load/{}.csv'.format(news_site_uid)], 
                        cwd='//.transform')


def _load():
    logger.info('Starting load process')
    for news_site_uid in news_site_uids:
        clean_data_filename = '{}.csv'.format(news_site_uid)
        subprocess.run(['python', 'sqlmain.py', clean_data_filename], cwd='.//load')
        subprocess.run(['rm', clean_data_filename], cwd='.//load')


if __name__ == '__main__':
    now = datetime.datetime.now().strftime("%Y_%m_%d")
    main()