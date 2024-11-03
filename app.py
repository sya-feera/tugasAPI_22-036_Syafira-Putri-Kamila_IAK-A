from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Data produk toko kelontong
products = [
    {"id": "1", "nama": "Beras", "harga": 12000, "stok": 100, "kategori": "Bahan Pokok"},
    {"id": "2", "nama": "Minyak Goreng", "harga": 14000, "stok": 50, "kategori": "Bahan Pokok"},
    {"id": "3", "nama": "Gula Pasir", "harga": 8000, "stok": 75, "kategori": "Bahan Pokok"},
    {"id": "4", "nama": "Telur", "harga": 2000, "stok": 200, "kategori": "Bahan Pokok"},
    {"id": "5", "nama": "Indomie Goreng", "harga": 3500, "stok": 150, "kategori": "Makanan Instan"},
    {"id": "6", "nama": "Kopi Sachet", "harga": 1500, "stok": 100, "kategori": "Minuman"},
    {"id": "7", "nama": "Sabun Mandi", "harga": 3500, "stok": 80, "kategori": "Perlengkapan Mandi"},
    {"id": "8", "nama": "Pasta Gigi", "harga": 4500, "stok": 60, "kategori": "Perlengkapan Mandi"},
    {"id": "9", "nama": "Deterjen", "harga": 5000, "stok": 70, "kategori": "Pembersih"},
    {"id": "10", "nama": "Shampoo", "harga": 12000, "stok": 45, "kategori": "Perlengkapan Mandi"},
    {"id": "11", "nama": "Teh Celup", "harga": 6000, "stok": 90, "kategori": "Minuman"},
    {"id": "12", "nama": "Susu Kental Manis", "harga": 7000, "stok": 55, "kategori": "Minuman"},
    {"id": "13", "nama": "Kecap Manis", "harga": 4000, "stok": 65, "kategori": "Bumbu Dapur"},
    {"id": "14", "nama": "Saus Sambal", "harga": 3500, "stok": 70, "kategori": "Bumbu Dapur"},
    {"id": "15", "nama": "Tepung Terigu", "harga": 9000, "stok": 85, "kategori": "Bahan Pokok"}
]

# Resource untuk menampilkan semua produk
class ProductList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(products),
            "products": products
        }
    
    def post(self):
        data = request.get_json()
        new_id = str(len(products) + 1)
        new_product = {
            "id": new_id,
            "nama": data.get('nama'),
            "harga": data.get('harga'),
            "stok": data.get('stok'),
            "kategori": data.get('kategori')
        }
        products.append(new_product)
        return {
            "error": False,
            "message": "Produk berhasil ditambahkan",
            "product": new_product
        }

# Resource untuk detail, update, dan delete produk
class ProductDetail(Resource):
    def get(self, product_id):
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            return {
                "error": False,
                "message": "success",
                "product": product
            }
        return {"error": True, "message": "Produk tidak ditemukan"}, 404

    def put(self, product_id):
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            data = request.get_json()
            product['nama'] = data.get('nama', product['nama'])
            product['harga'] = data.get('harga', product['harga'])
            product['stok'] = data.get('stok', product['stok'])
            product['kategori'] = data.get('kategori', product['kategori'])
            return {
                "error": False,
                "message": "Produk berhasil diupdate",
                "product": product
            }
        return {"error": True, "message": "Produk tidak ditemukan"}, 404

    def delete(self, product_id):
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            products.remove(product)
            return {
                "error": False,
                "message": "Produk berhasil dihapus"
            }
        return {"error": True, "message": "Produk tidak ditemukan"}, 404

# Resource untuk pencarian produk
class ProductSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [p for p in products if query in p['nama'].lower() or query in p['kategori'].lower()]
        return {
            "error": False,
            "founded": len(result),
            "products": result
        }

# Mendaftarkan resource ke API
api.add_resource(ProductList, '/products')
api.add_resource(ProductDetail, '/products/<string:product_id>')
api.add_resource(ProductSearch, '/products/search')

if __name__ == '__main__':
    app.run(debug=True)
