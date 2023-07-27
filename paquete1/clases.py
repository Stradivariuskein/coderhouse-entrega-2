from datetime import datetime

# productos para probar
products = {
    "1": {"title": "Remera Adidas", "price": 1264.25},
    "2": {"title": "Zapatillas Nike", "price": 500.75},
    "3": {"title": "Pantalón Levi's", "price": 999.99},
    "4": {"title": "Camisa Ralph Lauren", "price": 49.95},
    "5": {"title": "Gorra Puma", "price": 749.00},
    "6": {"title": "Shorts Under Armour", "price": 199.50},
    "7": {"title": "Bufanda Tommy Hilfiger", "price": 299.99},
    "8": {"title": "Chaqueta Columbia", "price": 799.00},
    "9": {"title": "Vestido Calvin Klein", "price": 109.95},
    "10": {"title": "Bolso Gucci", "price": 599.00},
    "11": {"title": "Gafas de sol Ray-Ban", "price": 299.00},
    "12": {"title": "Reloj Casio", "price": 179.99}
}

def divider_print(text):
    print("\n============================================================")
    print(f"**{text}**")
    print("============================================================")

class Persona: # clase base para cliente
    def __init__(self, name, surname, adres) -> None:
        self.name = name
        self.surname = surname
        self.adres = adres

    def __str__(self):
        return f"Name: {self.name} {self.surname}\nAdres: {self.adres}"


class Cliente(Persona):
    def __init__(self, name, surname, adres, cash, id) -> None:
        super().__init__(name, surname, adres)
        self.cash = cash
        self.id = id

    def __str__(self):
        return f"ID: {self.id}\n{super().__str__()}\nCash: {self.cash}"
    
    def buy_product(self, product): # verifica si su saldo es suficiente para para pagar y se lo descuenta
        if self.cash > product.price:
            self.cash -= product.price
            return True
        else:
            print(f"No posee saldo suficiente\nSu saldo: {self.cash}")
            return False
    
    def add_cash(self, product): #agrega efectivo a la cartera
        self.cash += product.price 

    def make_order(self): # hace un pedido
        order = OrderProduct(self.id)
        print("=======================**Pedido**=======================")
        print(f"Nombre: {self.name} {self.surname}\t ID: {self.id}")
        print("========================================================")
        while True:
            pro_id = input(f"Ingrese el ID del producto (IDs: 1 - 12, 0 para salir): ").strip()
            if pro_id != "0":
                if pro_id in products:
                    amount = input("Ingrese la cantidad: ").strip()
                    if pro_id != "":
                        product = Product(pro_id)
                        if product != None:
                            order.append(product, amount)
                else:
                    print(f"ID {pro_id} no existe")
                        
            else: # si el id es = 0 termia el bucle
                break
        return order


    

class Product: # clase producto con sus atributos y metodos
    def __init__(self, id, title = None, price = None) -> None: 
        try: # si el producto existe y los parametros son None obtine el producto.
            id = str(id)
            product = products[id]
            self.id = id 
            if title == None:
                self.title = product["title"]
            else: # si no es None se utliza el parametro por mas q el id exista esto permite mas flexibilidad para reescribir temporalmente el atributo
                self.title = title
            if price == None:
                self.price = product["price"]
            else:
                self.price = price
        except KeyError: # si la key no existe crea el producto. Para crear un producto hay q pasarle todos los parametros
            if title != None and price != None:
                self.id = id 
                self.title = title
                self.price = price
                product[id] = {"title": title, "price": price}
                print("Producto creado exitosamente")
            else:
                print(f"El ID {id} no existe")
                return None
        except Exception as e:
            print(f"Error inesperado: {type(e)}")

    def __str__(self) -> str:
        return f"ID: {self.id} || Title: {self.title} || Price: {self.price}"

    def increse_percent(self, percent): # aumento de precio por porsentaje
        if percent < 1:
            self.price = self.price * (percent + 1)            
        else:
            percent = (percent/100) + 1
            if 1 < percent <= 2:
                self.price = self.price * percent
            else:
                return 0
        return self.price
    
    def make_dic(self): # ver para sacar
        return {self.id: {"price": self.price, "title": self.title}}
    
class ListProduct: # lista con los productos. se utiliza para la clase como base para la clase OrderProduct
    def __init__(self, list_p = None) -> None:
        if isinstance(list_p, list): # validacion
            self.products = list_p 
        elif list_p == None:
            self.products = []
        else:
            raise TypeError
    
    def __str__(self) -> str:
        text = ""
        for p in self.products:
            text += f"{p}\n"
            text += "--------------------------------------------\n"
        return text[:-1]
    
    def __len__(self) -> int:
        return len(self.products)
    
    def append(self, product): # agrega 1 producto a la lista
        if isinstance(product, Product): # validacion
            self.products.append(product)
        else:
            raise TypeError
    
    def del_item(self, id) -> bool: # elimina un item
        if isinstance(id, str):
            for p in self.products:
                if id == p.id:
                    self.products.remove(p)
                    return True
        else:
            raise TypeError
        return False
    

class OrderProduct(ListProduct): # clase pedido q hereda de listProduct. esta clase contine una lista con todos los productos y las cantidades peedidas por el cliente
    def __init__(self, cli_id, amounts=None, list_p=None) -> None:
        super().__init__(list_p)
        if amounts != None:
            self._amounts = amounts
        else:
            self._amounts = []
        if not self.valid_products_amounts():
            raise IndexError
        self.cli_id = cli_id
        self.date = datetime.now()

    def valid_products_amounts(self) -> bool: # valida si la longitud de las dos listas son iguales
        if len(self.products) == len(self._amounts):
            return True
        return False


    def append(self, product, amount) -> bool: # agrega un iteem al pedido
        if self.valid_products_amounts():
            super().append(product)   
            self._amounts.append(int(amount))
            return True
        return False
    
    def total_amount(self) -> float: # la suma total de todo el pedido en $
        len_p = len(self.products)
        total = 0
        for i in range(len_p):
            total += self.products[i].price * self._amounts[i]
        return total
    
    def del_item_with_id(self, id) -> bool: # elimina el primer elemento con el id
        len_p = len(self.products)
        for i in range(len_p):
            if self.products[i].id == id:
                del self.products[i]
                del self._amounts[i]
                return True
        return False
    
    def del_item_with_index(self, index): # elimina el elemento atravez del index
        try:
            index = int(index) 
            if index != 0:
                index -= 1
            del self.products[index]
            del self._amounts[index]

        except IndexError:
            print(f"El item {index} no existe, ultimo item es {len(self)}")
        except Exception as e:
            print(f"Error inesperado: {type(e)}")
    
    def __str__(self) -> str:
        len_p = len(self.products)
        text = f"========================**Pedido**=========================\nCliente ID: {self.cli_id}\tFecha: {self.date}\n===========================================================\n"
        for i in range(len_p):
            text += f"{self.products[i]} || amount: {self._amounts[i]}\n"
            text += "------------------------------------------------------------\n"
        return f"{text[:-1]}\nTotal: {self.total_amount()}"
