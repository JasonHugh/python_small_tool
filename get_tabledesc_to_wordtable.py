#coding:utf-8
#把数据库中的表结构导出到word的表格中，完成设计文档
#不会用win32com操作word样式
import MySQLdb,config
from win32com.client import Dispatch,constants

db_name = "crawlerdb_update"
db = MySQLdb.connect(host=config.db_host,port=config.db_port,user=config.db_user,passwd=config.db_pwd,db=db_name,charset="utf8")
cursor = db.cursor()
	
def get_tables(cursor,db_name):
	sql = "select table_name,table_comment from information_schema.tables where table_schema = '" + db_name + "'"
	cursor.execute(sql)
	result = cursor.fetchall()
	tables = {}
	for r in result:
		tables[r[0]] = r[1]
	return tables

def get_table_desc(cursor,db_name,table_name):
	sql = "select column_name,column_type,column_default,is_nullable,column_comment from information_schema.columns where table_schema = '" + db_name + "' and table_name = '" + table_name + "'" 
	cursor.execute(sql)
	result = cursor.fetchall()
	return result

tables = get_tables(cursor,db_name)

word = Dispatch('Word.Application')
word.Visible = 1  
word.DisplayAlerts = 0 
doc = word.Documents.Add()
r = doc.Range(0,0)
r.Style.Font.Name = u"Verdana"
r.Style.Font.Size = "9"

for k,table_name in enumerate(tables):
	tables_desc = get_table_desc(cursor,db_name,table_name)

	print r.Start
	r.InsertBefore("\n" + tables[table_name] + " " + table_name)
	table = r.Tables.Add(doc.Range(r.End,r.End),len(tables_desc) + 1,5)
	table.Rows[0].Cells[0].Range.Text = u"列"
	table.Rows[0].Cells[1].Range.Text = u"类型"
	table.Rows[0].Cells[2].Range.Text = u"默认值"
	table.Rows[0].Cells[3].Range.Text = u"是否为空"
	table.Rows[0].Cells[4].Range.Text = u"列备注"
	for i,column in enumerate(tables_desc):
		for j,col in enumerate(column):
			if col == None:
				col = "(NULL)"
			table.Rows[i+1].Cells[j].Range.Text = col


	r = doc.Range(table.Range.End,table.Range.End)

	break

