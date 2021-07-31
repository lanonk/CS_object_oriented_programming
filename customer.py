class Customer:
        
        #the initilized variables for this class
        def __init__(self):
            self.id = " "
            self.name = " "
            self.order = []
          

        #counts the number of orders a customer has---can also us len function    
        def get_order_count(self):
            count = 0
            for i in self.order:
                count += 1
            return count
        
        #returns the total amount a customer pays
        def get_total(self):
            total = 0 #this is not returning a total
            for order in self.order:
                total += (order.get_total())
            return total
                
                
        # adds orders to the list as a cutomer orders more items
        def add_order(self, new_order):
            self.order.append(new_order)
         # the display functions below give all the info for the customer and their orders   
        def display_summary(self):
            print("Summary for customer: {}".format(self.id))
            print("Name: {}".format(self.name))
            print("Orders: {}".format(self.get_order_count()))
            print("Total: ${:.2f}".format(self.get_total()))
            
        def display_receipts(self):
            print("Detailed receipts for customer {}:".format(self.id))
            print("Name: {}".format(self.name))
            print()
            for customer in self.order:
                customer.display_receipt()
                print()