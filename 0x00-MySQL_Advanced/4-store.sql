-- Defines trigger to decrement item quantity after new order insertion.
-- Allows negative quantities.

CREATE TRIGGER decrease_quant AFTER INSERT ON orders
FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;
