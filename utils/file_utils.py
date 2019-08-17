def get_last_product():
    try:
        product_file = open("recent_product.txt", "r")
        product_name = product_file.read()
        product_file.close()
    except FileNotFoundError:
        product_name = ''
    return product_name

def write_last_product(product_name):
    product_file = open("recent_product.txt", "w")
    product_file.write(product_name)
    product_file.close()
