#coding:utf-8
#直接在mysql中，把crawlerdb里的数据导入crawler_update中
#两个库的区别：表名不一样，要相互对应；有些字段不一样，要进行处理
#使用时记得把config加上
import MySQLdb,config

def get_tables(db_name):
	db = MySQLdb.connect(host=config.db_host,port=config.db_port,user=config.db_user,passwd=config.db_pwd,db=db_name,charset="utf8")
	cursor = db.cursor()
	#获取所有表
	sql = "show tables"
	cursor.execute(sql)
	result = cursor.fetchall()
	tables = [r[0] for r in result]
	return tables

from_tables = get_tables("crawlerdb")
to_tables = get_tables("crawlerdb_update")
#手工重新对应table顺序------------------------
from_tables = ['comment_count_need','product_comments_statistics','product_comments_statistics1',u'comment_count_jd', u'comment_count_kaola', u'comment_count_tmall', u'comment_count_yintai', u't_repo_keyword', u't_crawler_client', u't_crawler_content', u't_crawler_list_url', u't_crawler_source', u't_monitor_result', u't_monitor_task', u't_repo_extend_keyword', u't_repo_sentiment', u'product_comments_jd', u'product_comments_kaola', u'product_comments_tmall', u'product_comments_yintai', u'product_info', u'product_info_jd', u'product_info_kaola', u'product_info_tmall', u'product_info_yintai', u'product_task', u't_repo_class1', u't_repo_class2', u't_repo_extend_class', u't_repo_extend_extend', u't_crawler_newsurl', u't_e_commerce_public_opinion',  u't_negative_percent_point', u'product_comments_need', u'product_info_need', u't_repo_product']
to_tables = [u'T_BUSI_COMMENT_COUNT_NEED', u'T_BUSI_PRODUCT_COMMENTS_STATISTICS', u'T_BUSI_PRODUCT_COMMENTS_STATISTICS1',u'T_BASE_COMMENT_COUNT_JD', u'T_BASE_COMMENT_COUNT_KAOLA', u'T_BASE_COMMENT_COUNT_TMALL', u'T_BASE_COMMENT_COUNT_YINTAI', u'T_BASE_COMMENT_KEYWORD', u'T_BASE_CRAWLER_CLIENT', u'T_BASE_CRAWLER_CONTENT', u'T_BASE_CRAWLER_RULE', u'T_BASE_CRAWLER_SOURCE', u'T_BASE_MONITOR_RESULT', u'T_BASE_MONITOR_TASK', u'T_BASE_NEWS_KEYWORD', u'T_BASE_NEWS_SENTIMENT', u'T_BASE_PRODUCT_COMMENTS_JD', u'T_BASE_PRODUCT_COMMENTS_KAOLA', u'T_BASE_PRODUCT_COMMENTS_TMALL', u'T_BASE_PRODUCT_COMMENTS_YINTAI', u'T_BASE_PRODUCT_INFO', u'T_BASE_PRODUCT_INFO_JD', u'T_BASE_PRODUCT_INFO_KAOLA', u'T_BASE_PRODUCT_INFO_TMALL', u'T_BASE_PRODUCT_INFO_YINTAI', u'T_BASE_PRODUCT_TASK', u'T_BASE_REPO_CLASS1', u'T_BASE_REPO_CLASS2', u'T_BASE_REPO_EXTEND_CLASS', u'T_BASE_REPO_EXTEND_EXTEND', u'T_BUSI_CRAWLER_NEWSURL', u'T_BUSI_E_COMMERCE_PUBLIC_OPINION', u'T_BUSI_NEGATIVE_PERCENT_POINT', u'T_BUSI_PRODUCT_COMMENTS_NEED', u'T_BUSI_PRODUCT_INFO_NEED', u'T_BUSI_REPO_PRODUCT']

db = MySQLdb.connect(host=config.db_host,port=config.db_port,user=config.db_user,passwd=config.db_pwd,db="crawlerdb",charset="utf8")
cursor = db.cursor()
for i,from_table in enumerate(from_tables):
	sql = "show columns from " + from_table
	cursor.execute(sql)
	result = cursor.fetchall()
	columns = [r[0] for r in result]
	columns_str = ",".join(columns)
	to_columns = columns_str.replace("edit_time","save_time")
	from_columns = columns_str.replace("edit_time","edit_time save_time")

	sql = "insert into crawlerdb_update." + to_tables[i] + "(" + to_columns + ") select " + from_columns + " from crawlerdb." + from_table
	print sql

	try:
		cursor.execute(sql)
		db.commit()
	except Exception, e:
		print "-----------------error-------------------\n"

