class OrderManager:
    def __init__(self, orders_file):
        self.orders_file = orders_file

    def create_order(self, user, items, address, payment):
        order_id = str(int(time.time()))
        with open(self.orders_file, 'a') as file:
            file.write(f"{order_id},{user},{'-'.join(items)},{address}|{payment},pending\n")
        return order_id

    def get_order(self, order_id):
        try:
            with open(self.orders_file, 'r') as file:
                for line in file:
                    order_data = line.strip().split(',')
                    if order_data[0] == order_id:
                        address_payment = order_data[3].split('|')
                        return {
                            'order_id': order_data[0],
                            'user': order_data[1],
                            'items': order_data[2].split('-'),
                            'address': address_payment[0],
                            'payment': address_payment[1],
                            'status': order_data[4]
                        }
        except FileNotFoundError:
            return None
        return None