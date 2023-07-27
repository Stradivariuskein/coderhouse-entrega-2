from paquete1.clases import *

if __name__ == "__main__":
    divider_print("cliente creado")
    cli1 = Cliente("Pepe", "Gordoni", "cuchacucha 123", 30000, "1")
    print(f"str de cliente:\n{cli1}")
    
    divider_print("Hacer un peddo")
    order = cli1.make_order()
    print(order)
    
    divider_print("item 1 eliminado")
    order.del_item_with_index(1)
    print(order)
    
    divider_print("logitud del pedido")
    print(f"Longitud del pedido: {len(order)}")
    
    divider_print("creacion de un poducto")
    prod1 = Product(5)
    print(f"prod1: {prod1}\n en este caso lo obtiene de la variable global products")
    
    divider_print("Creacion del prod2 sin el precio")
    prod2 = Product(5,title="Anillo de mordor")
    print(f"prod1: {prod2}\n en este caso sobreescrivimos solo el titulo")
    
    divider_print("Creacion del prod3 sin el titulo")
    prod3 = Product(5,price=5600.30)
    print(f"prod1: {prod3}\n en este caso sobreescrivimos solo el precio")
    

