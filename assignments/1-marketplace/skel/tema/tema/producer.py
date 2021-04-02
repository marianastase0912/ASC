"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from time import sleep
from threading import Thread


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.producer_id = self.marketplace.register_producer()

    def run(self):
        while True:
            for product in self.products:
                # get the name of the product
                # get the number of products to be prepared
                # get the time it takes to prepare them
                product_name = product[0]
                no_products = product[1]
                wait_prepare_time = product[2]
                # attempt to publish the product in the Marketplace
                # if successful, wait the allocated time
                # otherwise wait to repuplish the product
                for _ in range(no_products):
                    publish_product = self.marketplace.publish(str(self.producer_id), product_name)

                    if publish_product is False:
                        sleep(self.republish_wait_time)
                    else:
                        sleep(wait_prepare_time)
