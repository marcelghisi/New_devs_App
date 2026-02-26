# Monetary amounts are stored as NUMERIC(10, 3) to allow sub-cent precision tracking.
# See: database/schema.sql (reservations.total_amount)
MONETARY_DECIMAL_PLACES = 3
