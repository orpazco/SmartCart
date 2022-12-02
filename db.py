import sqlite3
import uuid


class SmartCartDB:
    def __init__(self):
        self.con = sqlite3.connect("smart-cart.db", check_same_thread=False)
        self.cursor = self.con.cursor()
        self._next_pid = 0
        self._create_tables()
        self._update_products()

    def add_new_product(self, product_name: str, cost: float):
        self.cursor.execute("""INSERT OR IGNORE INTO groceries(product_id,product_name,cost)
                                VALUES(?,?,?)""", (self._next_pid, product_name, cost))
        self.con.commit()
        self._next_pid += 1

    def add_new_customer(self, cid: str, name: str, active: bool):
        self.cursor.execute("""INSERT INTO customers(id,name,active) VALUES(?,?,?)""", (cid, name, int(active)))
        self.con.commit()

    def add_item_to_cart(self, cid: int, pid: str):
        self.cursor.execute("""INSERT INTO carts(customer_id,product_id) VALUES(?,?)""", (cid, pid))
        self.con.commit()

    def get_cart(self, cid):
        self.cursor.execute(f"""SELECT groceries.product_name, groceries.cost
                                            FROM groceries
                                            INNER JOIN carts ON carts.product_id=groceries.product_id
                                            WHERE carts.customer_id=?;""", (str(cid),))
        return self.cursor.fetchall()

    def get_cost(self, product_name):
        self.cursor.execute("""SELECT cost
        FROM groceries
        """)

    def _create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS customers (
                                        id text PRIMARY KEY,
                                        name text NOT NULL
                                    );""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS carts (
                                        customer_id text,
                                        product_id integer NOT NULL,
                                        FOREIGN KEY (customer_id) REFERENCES customers (id),
                                        FOREIGN KEY (product_id) REFERENCES groceries (product_id)
                                    );""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS groceries (
                                        product_id integer PRIMARY KEY,
                                        product_name text NOT NULL,
                                        cost real NOT NULL
                                    );""")
        self.con.commit()

    def close(self):
        self.cursor.close()
        self.con.close()

    def _update_products(self):
        self.add_new_product("apple", 5.40)
        self.add_new_product("banana", 3.33)
        self.add_new_product("bread", 12.0)
        self.add_new_product("milk", 13.40)
        self.add_new_product("chocolate", 18.90)
        self.add_new_product("eggs", 21.99)


db_session = SmartCartDB()
