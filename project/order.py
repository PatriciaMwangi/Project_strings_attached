from __init__ import conn,cursor

class Order:
    all={}
    category_and_yarn_price={
        'Mesh Pants':{'Yarn':"Cotton",'price':20},
        'skirts':{"Yarn":'Wool','price': 30},
        'Tops':{'Yarn':'Acrylic','price':25},
        'Sweaters':{'Yarn':'Alpaca','price':40},
        'Bags':{'Yarn':'Nylon','price':15}
    }
    def __init__(self,number_of_yarn,hours_spent,id=None):
      
        self._number_of_yarn=None
        self.number_of_yarn=number_of_yarn
        self._hours_spent=None
        self.hours_spent=hours_spent
        
        if id is None:
            self.id=max(self.all.keys(),default=0)+1
        else:
            self.id=id

        type(self).all[self.id]=self
    def __repr__(self) -> str:
        return f"Orders(id={self.id},number_of_yarn={self.number_of_yarn},hours_spent={self.hours_spent})"

    @classmethod
    def get_yarn_and_price(cls,category):
        if category in cls.category_and_yarn_price:
            return cls.category_and_yarn_price[category]
        else:
            raise ValueError(f"Category {category} is not available")
    @classmethod
    def orders(cls):
        return list(cls.all.values())
    
    @property
    def yarn(self):
        return self._number_of_yarns
    @yarn.setter
    def yarn(self,number_of_yarn):
        if not isinstance(number_of_yarn,int) or number_of_yarn < 1:
            raise ValueError("Must be a positive integer")
    @property
    def hours(self):
        return self._hours_spent
    @hours.setter
    def hours(self,hours_spent):
        if not isinstance(hours_spent,int) or hours_spent < 1:
            raise ValueError("Must be a positive integer ")
        self._hours_spent=hours_spent

    def customer_details(self):
        from customers import Customer
        for customer in Customer.all.values():
            if customer.order_id==self.id:
                return{
                    'name':customer.name,
                    'size':customer.size,
                    'category':customer.category,
                    'color':customer.color
               }

        
    def price(self,category):
        yarn_price=Order.get_yarn_and_price(category)
        total=(self.hours_spent * 150)+(self.number_of_yarn*yarn_price['price'])
        return total
    
    @classmethod
    def create_table(cls):
        sql="""
            CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number_of_yarn INTEGER,
            hours_spent INTEGER)"""
        cursor.execute(sql)
        conn.commit()

    @classmethod
    def drop_table(cls):
        sql="""
            DROP TABLE IF EXISTS orders    
            """
        cursor.execute(sql)
        conn.commit()

    def save(self):
        sql="""
            INSERT INTO orders(number_of_yarn,hours_spent) VALUES(?,?)"""
        cursor.execute(sql,(self.number_of_yarn,self.hours_spent))
        conn.commit()
        self.id=cursor.lastrowid
        type(self).all[self.id]=self

    @classmethod
    def create_row(cls,number_of_yarn,hours_spent):
        """Initialize a new Order object and save the object to the database"""
        order=Order(number_of_yarn,hours_spent)
        order.save()
        return order
    
    def update(self):
        """update the table row corresponding to the current order object"""
        sql="""
            UPDATE orders
            SET number_of_yarn= ?, hours_spent= ?
            WHERE id =?
            """
        cursor.execute(sql,(self.number_of_yarn,self.hours_spent,self.id))
        conn.commit()
    @classmethod
    def instance_from_db(cls,row):
        order = cls.all.get(row[0])
        if order:
            order.number_of_yarn=row[1]
            order.hours_spent=row[2]
        else:
            order.id=row[0]
            order=cls(row[1],row[2])
            cls.all[order.id]=order
        return order
    
    def customer(self):
        """return the list of orders associated with the current customer object"""
        from customers import Customer
        sql="""SELECT * FROM customers 
            WHERE order_id = ?
            """
        
        cursor.execute(sql,(self.id,))
        rows=cursor.fetchall()
        return[Customer.instance_from_db(row) for row in rows]
    
Order.drop_table()
Order.create_table()
order=Order.create_row(number_of_yarn=3,hours_spent=5)
order1=Order.create_row(number_of_yarn=13,hours_spent=10)
order2=Order(id=2,number_of_yarn=1,hours_spent=24)
#op=order2.customer()
o=Order.get_yarn_and_price('Tops')
#op=order2.customer_details()
#print(op)

#for c in Order.all.items():
   # print(c)
c=Order.orders()
print(c)

print(order.price('Mesh Pants'))

    

    
            
        

    

    

        

    




    