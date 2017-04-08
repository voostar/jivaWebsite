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

	def db_validation(self):
		# dy2018
		sql = """CREATE TABLE movies_dy2018_info (
			name  TEXT(300) NOT NULL,
			url  TEXT(300),
			hash TEXT(300),
			include_date DATE)"""
		print("checking movies_dy2018_info validation")
		try:
			self.cursor.execute(sql)
			print("created database: movies_dy2018_info")
		except:
			print("database movies_dy2018_info existed")
		# links
		sql = """CREATE TABLE movies_dy2018_links (
			hash  TEXT(300) NOT NULL,
			link  TEXT(300))"""
		print("checking movies_dy2018_links validation")
		try:
			self.cursor.execute(sql)
			print("created database: movies_dy2018_links")
		except:
			print("database movies_dy2018_links existed")


	def execute_command(self, sql):
		self.cursor.execute(sql)
		self.db.commit()
		return True

	def add_movie_item(self, **args):
		sql = "INSERT INTO movies_dy2018_info(name, url, hash, include_date) VALUES ('{name}', '{url}', '{hash}', '{include_date}');".format(
		 	name=args["name"],
		 	url=args["url"],
		 	hash=args["hash"],
		 	include_date=args["include_date"])
		print(sql)
		self.execute_command(sql)

	def search_movie_item(self, filter_item_tuple):
		sql = "SELECT * FROM movies_dy2018_info WHERE {}='{}';".format(filter_item_tuple[0], filter_item_tuple[1])
		print(sql)
		self.execute_command(sql)

		return self.cursor.fetchall()

	def get_all_movie_items(self):
		sql = "SELECT * FROM movies_dy2018_info"
		self.execute_command(sql)

		return self.cursor.fetchall()

	def add_download_link(self, movie_hash, movie_link):
		sql = "INSERT INTO movies_dy2018_links(hash, link) VALUES ('{hash}', '{link}');".format(
		 	hash=movie_hash,
		 	link=movie_link)
		print(sql)
		self.execute_command(sql)

	def flush_table(self, table_name):
		sql = "DELETE * FROM {}".format(table_name)

		self.execute_command(sql)