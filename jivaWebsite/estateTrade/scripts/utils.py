# -*- coding: utf-8 -*-
import pymysql

class mysqlClient:
	def __init__(self):
		self.db = pymysql.connect(host="localhost",user="home",passwd="home",db="home",charset="utf8")
		self.cursor = self.db.cursor()
		# self.db_validation()

	def __enter__(self):
		return mysqlClient()

	def __exit__(self):
		if self.cursor:
			self.cursor.close()
			self.db.close()

	def execute_command(self, sql):
		self.cursor.execute(sql)
		self.db.commit()
		return True

	def add_item(self, **args):
		sql = "INSERT INTO estateTrade_estatetrade(district, acreage_amount, apartment_amount, trade_date) VALUES ('{district}', '{acreage_amount}', '{apartment_amount}', '{trade_date}');".format(
		 	district=args["district"],
		 	acreage_amount=args["acreage_amount"],
		 	apartment_amount=args["apartment_amount"],
		 	trade_date=args["trade_date"])
		# print(sql)
		self.execute_command(sql)

	def search_item(self, filter_item_tuple):
		sql = "SELECT * FROM estateTrade_estatetrade WHERE {}='{}';".format(filter_item_tuple[0], filter_item_tuple[1])
		print(sql)
		self.execute_command(sql)

		return self.cursor.fetchall()

	def get_all_items(self):
		sql = "SELECT * FROM estateTrade_estatetrade"
		self.execute_command(sql)

		return self.cursor.fetchall()

	def flush_table(self, table_name):
		sql = "DELETE * FROM {}".format(table_name)

		self.execute_command(sql)

	def get_last_trade_date(self):
		sql = "SELECT distinct(trade_date) FROM home.estateTrade_estatetrade order by trade_date DESC limit 1;"

		self.execute_command(sql)

		return self.cursor.fetchone()