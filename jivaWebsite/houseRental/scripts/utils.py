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
		sql = "INSERT INTO houseRental_house_retal_info(url, name, district, street, estate, house_type, acreage, price, source, include_date) VALUES ('{url}', '{name}', '{district}', '{street}', '{estate}', '{house_type}', '{acreage}', '{price}', '{source}', '{include_date}');".format(
		 	url=args["url"],
		 	name=args["name"],
		 	district=args["district"],
		 	street=args["street"],
		 	estate=args["estate"],
		 	house_type=args["house_type"],
		 	acreage=args["acreage"],
		 	price=args["price"],
		 	source=args["source"],
		 	include_date=args["include_date"])
		# print(sql)
		self.execute_command(sql)

	def search_item(self, filter_item_tuple):
		sql = "SELECT * FROM houseRental_house_retal_info WHERE {}='{}';".format(filter_item_tuple[0], filter_item_tuple[1])
		# print(sql)
		self.execute_command(sql)

		return self.cursor.fetchall()

	def get_all_items(self):
		sql = "SELECT * FROM houseRental_house_retal_info"
		self.execute_command(sql)

		return self.cursor.fetchall()

	def flush_table(self, table_name):
		sql = "DELETE * FROM {}".format(table_name)

		self.execute_command(sql)