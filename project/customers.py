from __init__ import conn,cursor
from collections import Counter
class Customer:
    all={}
    category_available=['Mesh pants','skirts','tops','sweaters','bags']

    def __init__(self,name,size,color,category,order_id,id=None):
        self._name=None#initialize the private atttribute i.e just used within the class cannot be accessed outside of it
        self._size=None
        self._color=None
        self._category=None

        self.name=name#triggers validation the validation i.e name.setter
        self.size =size
        self.color=color
        self.category=category
        self.order_id=order_id
        if id is None:
            self.id=max(self.all.keys(),default=0)+1
        else:
            self.id=id

        type(self).all[self.id] = self
        #print(f"Customers added: {self}")
    
    def __repr__(self):
        return f"Customer(id={self.id}, name={self.name}, size={self.size}, color={self.color}, category={self.category}, order_id={self.order_id})"


    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,name):
        if not  isinstance(name,str) or not (3<= len(name) <= 50):
            raise ValueError('Name must be of type string and between 5 and 50 characters')
        self._name=name

    @property
    def category(self):
        return self._category
    @category.setter
    def category(self,category):
        if category not in type(self).category_available:
            raise ValueError(f"sorry, for now i only crotchet:{', '.join(type(self).category_available)}")
        self._category=category

    def category_chosen(self):
        print(f"Finding customers with category: {self.category}")
        customers_with_same_category = [customer for customer in type(self).all.values() if customer.category == self.category]
        print(f"Customers who ordered from the same category: {customers_with_same_category}")
        return customers_with_same_category
    def category_count(self):
        categories= Counter(customer.category for customer in type(self).all.values())
        print(f"Number of customers who ordered chosen category:{categories}")
        return categories

    @property 
    def size(self):
        return self._size
    @size.setter
    def size(self,size):
        if not isinstance(size,list) or not all(isinstance(i,int) for i in size) or len(size) < 3:
            raise ValueError("Expected 3 values(chest,hips and waist) all in type integer")
        if not all(i > 0 for i in size):
            raise ValueError("Value must be a positive integer")
        self._size=size

    def choose_size_top(self,burst,hips,waist):
        if 32 <=  burst <=33 and 33<= hips <= 35 and 24<= waist <= 25:
            self.size=[burst,hips,waist]
            self._category='XS'
        elif 34 <= burst <= 35 and 36 <= hips <= 38.4 and 26 <= waist <= 27:
            self.size=[burst,hips,waist]
            self._category='S'
        elif 36 <= burst <= 37.4 and 38.5 <= hips <= 39.5 and 28<= waist <=29:
            self.size=[burst,hips,waist]
            self._category='M'
        elif 38.5 <= burst <= 40 and 39.6 <= hips <= 43 and 30 <= waist <= 32:
            self.size=[burst,hips,waist]
            self._category='L'
        elif 41 <= burst <= 60 and 44 <= hips <= 60 and 33<= waist <= 63:
            self.size=[burst,hips,waist]
            self._category= 'XL'
        else:
            raise ValueError("your measurements don't fit any group in our system so they will be printed as they are")
       
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self,color):
        if not isinstance(color,list) or not all(isinstance(i,str)for i in color) or len(color) < 1:
            raise ValueError("Must be in a list of at least one value and type string")
        self._color=[c.lower() for c in color]
    def count_color(self):
        colors_chosen= Counter(color for customer in type(self).all.values() for color in customer.color)
        print(f"Number of customers who requested the chosen color:{colors_chosen}")
        return colors_chosen if colors_chosen else None

    def order_details(self):
        from order import Order
        order=Order.all.get(self.order_id)
        if order:
            print("order include")
            return{
                'order_id':order.id,
                'number_of_yarn':order.number_of_yarn,
                'hours_spent':order.hours_spent,
                'total_amount':order.price(self.category)
            }
        return None




    @classmethod
    def create_table(cls):
        """insert every instance of the customer class in to the db"""
        sql="""
            CREATE TABLE IF NOT EXISTS customers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            size INTEGER,
            color TEXT[],
            category TEXT,
            order_id INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(id))
            """
        cursor.execute(sql)
        conn.commit()

    @classmethod
    def drop_table(cls):
        """Drop table that persists the Customers table"""
        sql="""
            DROP TABLE IF EXISTS customers
            """
        cursor.execute(sql)
        conn.commit()

    def save_row(self):
        """save an instance of customer class"""
        sql="""
            INSERT INTO customers(name,size,color,category,order_id) VALUES(?,?,?,?,?)
            """
        size_str=', '.join(map(str,self.size))
        color_str=', '.join(map(str,self.color))
        cursor.execute(sql,(self.name,size_str,color_str,self.category,self.order_id))
        conn.commit()
        self.id=cursor.lastrowid
        type(self).all[self.id]=self

    @classmethod
    def create_row(cls,name,size,color,category,order_id):
        customer=cls(name,size,color,category,order_id)
        customer.save_row()
        return customer
    
    def update(self):
        sql="""
            UPDATE customers
            SET name = ?, size=?, color = ?, category = ?, order_id =?
            WHERE id = ? 
            """
        size_str = ','.join(map(str, self.size))
        cursor.execute(sql,(self.name,size_str,self.color,self.category,self.order_id,self.id))
        conn.commit()
 
    def delete(self):
        sql="""
            DELETE FROM customers
            WHERE id = ?
            """
        try:
            cursor.execute(sql,(self.id,))
            conn.commit()

            del type(self).all[self.id]
            self.id=None
        
        except conn.Error as e:
            print(f"Error deleting customer with id {self.id}: {e}")


    @classmethod
    def instance_from_db(cls,row):
        customer=cls(
            name=row['name'],
            size=row['size'],
            color=row['color'],
            category=row['category'],
            order_id=row['order_id']
        )
        cls.all[customer.id]=customer
        return customer
   

    
customer=Customer("Patricia",[33,34,25],['red','white'],'tops',4)  
customer1 = Customer(name="Alice", size=[33,34,25],color=["Red", "Green"],category="skirts", order_id=1)
customer2 = Customer(name="Bob", size=[35,36,29], color=["Blue", "Yellow"], category="tops",order_id=1)
customer3 = Customer(name="Carol", size=[34,35,27], color=["Red", "Blue"], category="bags",order_id=3)
cc=customer1.order_details()
print(cc)




#for c in Customer.all.items():
#    print(c)


#print(Customer.all)
Customer.drop_table()
Customer.create_table()
row={'name':'Asake', 'size':[47,48,56],'color':['Brown'],'category':'sweaters','order_id':1}
customer_db=Customer.instance_from_db(row)
customer21=Customer.create_row(name="Alice", size=[33,34,25],color=["Red", "Green"],category="skirts", order_id=1)

customer=Customer.create_row(name="Bob", size=[35,36,29], color=["Blue", "Yellow"], category="tops",order_id=2)
customer3=Customer.create_row(name="Carol", size=[34,35,27], color=["Red", "Blue"], category="bags",order_id=3)
customer2 = Customer("Alices", [34, 26, 36], ["Blue"], "tops", 1,1)
c=customer2.update()
print(c)


cursor.execute("SELECT * FROM customers WHERE id =?",(customer2.id,))

#print(cursor.fetchone())
#print(customer_db)
#print(Customer.all)
#customer2.delete()
cursor.execute('SELECT * FROM customers WHERE id = ?',(customer2.id,))
#print(cursor.fetchone())
#n_c=customer2.order_details()
customer2.choose_size_top(33,34,25)
#print(customer3.category)
#print(n_c)

