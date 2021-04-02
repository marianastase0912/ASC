"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from time import sleep
from threading import Thread, currentThread

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        for cart in self.carts:
            # create new consumer id for the cart
            cart_id = self.marketplace.new_cart()

            for action in cart:
                # get the type of request
                # get the product name
                # get the number of items
                type_action = action["type"]
                product_id = action["product"]
                no_products = action["quantity"]
                # counter to keep track of the current number of items
                count_prod = 0

                while count_prod < no_products:
                    # call the marketplace function to add a product to the cart
                    if type_action == "add":
                        add_product = self.marketplace.add_to_cart(cart_id, product_id)
                        # if it is not available, wait to retry
                        while add_product is False:
                            sleep(self.retry_wait_time)
                            add_product = self.marketplace.add_to_cart(cart_id, product_id)

                        count_prod += 1
                    # # call the marketplace function to remove a product from the cart
                    elif type_action == "remove":
                        self.marketplace.remove_from_cart(cart_id, product_id)
                        count_prod += 1

            # print
            for prod in self.marketplace.place_order(cart_id):
                print("{} bought {}".format(currentThread().getName(), prod))
