import logging
from django.core.cache import cache
from .models import Property

logger = logging.getLogger(__name__)

def get_all_properties():
    # Try to get cached data from Redis
    properties = cache.get('all_properties')

    if properties is None:
        # If not found, fetch from DB
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        # Store in cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)

    return properties

def get_redis_cache_metrics():
    """
    Retrieves Redis cache hit/miss metrics and computes hit ratio.
    """
    try:
        # Connect to Redis
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        # Extract hit/miss stats
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        # Avoid division by zero
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 2)
        }

        # Log metrics for monitoring
        logger.info(f"Redis Cache Metrics: {metrics}")

        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0
        }
