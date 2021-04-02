"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        # dictionary of the list of products produced by each producer
        # id_producer -> list of products
        self.products_from_producers = {}

        #  dictionary to keep the id of the producer for a specific product
        #  product -> id producer
        self.product_id_producer = {}

        # lock to synchronize the addition in the product_id_producer
        self.lock_product_to_id = Lock()

        # lock to synchronize the add/remove operations
        self.lock_add_remove_product = Lock()

        # lock to syncronize the producer's ids
        self.lock_prod_producers = Lock()

        #  list with available products, common buffer
        self.available_products = []

        # dictionary linking the cart id to the list of products
        self.carts_lists = {}

        # variable to get an id for the producers
        self.register_id = 0

        # variable to get an id for the cart
        self.new_cart_id = 0

        # lock to syncronize adding new carts
        self.lock_carts = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # increment for each producer
        with self.lock_prod_producers:
            self.register_id += 1
            reg_id = self.register_id

        self.products_from_producers[reg_id] = []

        return reg_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # cast to integer
        producer_id_int = int(producer_id)

        # get the length of the producers's list(number of items)
        with self.lock_product_to_id:
            no_prod = len(self.products_from_producers[producer_id_int])

        # see if there is enough room for a new product, if not, return False
        if no_prod >= self.queue_size_per_producer:
            return False

        # if there is room for a new product
        # first map the product to the producer's id
        with self.lock_product_to_id:
            self.product_id_producer[product] = producer_id_int

        # add to the item to the list of products of the specific producer
        self.products_from_producers[producer_id_int].append(product)

        # add the product to the common buffer of available products
        self.available_products.append(product)

        return True


    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        # increment for each consumer
        with self.lock_carts:
            self.new_cart_id += 1
            id_cart = self.new_cart_id

        self.carts_lists[id_cart] = []

        return id_cart

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        # if the product is available in the common buffer, remove it from that list
        # remove it from the list of the specific producer
        # add the product to the list of the specific cart's list of products
        # if the product is not in the common buffer, return false
        with self.lock_add_remove_product:
            if product in self.available_products:
                self.available_products.remove(product)
                if product in self.products_from_producers[self.product_id_producer[product]]:
                    self.products_from_producers[self.product_id_producer[product]].remove(product)
                self.carts_lists[cart_id].append(product)

                return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # add the product to the list of the specific producer
        # remove the product from the cart's list
        # add the product to the common buffer
        with self.lock_add_remove_product:
            self.products_from_producers[self.product_id_producer[product]].append(product)

        self.carts_lists[cart_id].remove(product)
        self.available_products.append(product)


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.carts_lists[cart_id]
