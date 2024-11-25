from django.core.cache import cache

# Save stock data in Redis
def save_to_redis(symbol, stock_name, price, current_time):
    cache_key = f"stock:{symbol}"
    cache_value = {
        "stock_name": stock_name,
        "price": float(price),
        "current_time": current_time
    }
    cache.set(cache_key, cache_value, timeout=300)  # Timeout in seconds (5 minutes)

# Retrieve stock data from Redis
def get_from_redis(symbol):
    cache_key = f"stock:{symbol}"
    return cache.get(cache_key)
