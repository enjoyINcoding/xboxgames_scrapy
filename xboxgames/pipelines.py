# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from hashlib import md5
from scrapy import log
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import time

class XboxgamesPipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        product_id = item['product_id']
        #now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        today = int(time.strftime("%Y%m%d"))
        spider.log(type(today))
        conn.execute("""SELECT EXISTS(
            SELECT id FROM g_price WHERE product_id = %s and scrapy_date= %s
        )""", (product_id,today ))
        ret = conn.fetchone()[0]

        if ret:
            conn.execute("""
                UPDATE g_price
                SET price=%s, full_price=%s
                WHERE id=%s
            """, (item['price'], 0, ret))
            spider.log("Item updated in db: %s %r" % (product_id, item))
        else:
            conn.execute("""
                INSERT INTO g_price ( product_id, title, title_zh, price,full_price,is_gold,scrapy_date,detail_url,country)
                VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)
            """, (product_id, item['title'], '', item['price'], 0,0 ,today , item['detail_url'], 'xg'))
            spider.log("Item stored in db: %s %r" % (product_id, item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item['url']).hexdigest()