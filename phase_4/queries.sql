-- 1. بازیابی تمام محصولات با قیمت‌ها و مقادیر موجودی:
SELECT ProductName, Price, StockQuantity
FROM Products;

-- 2. فهرست تمام دسته‌بندی‌ها:
SELECT CategoryName
FROM Categories;

-- 3. جزئیات کاربرانی که در تاریخ خاصی سفارش داده‌اند را بگیرید:
SELECT Users.Username, Users.Email, Orders.OrderDate
FROM Users
JOIN Orders ON Users.UserID = Orders.UserID
WHERE Orders.OrderDate = '2024-07-07';

-- 4. لیست محصولات با تخفیف‌های فعال فعلی:
SELECT Products.ProductName, Discounts.DiscountPercentage, Discounts.StartDate, Discounts.EndDate
FROM Products
JOIN Discounts ON Products.ProductID = Discounts.ProductID
WHERE DATE('now') BETWEEN Discounts.StartDate AND Discounts.EndDate;

-- 5. بازیابی تمام نظرات برای یک محصول خاص:
SELECT Users.Username, Reviews.Rating, Reviews.Comment, Reviews.ReviewDate
FROM Reviews
JOIN Users ON Reviews.UserID = Users.UserID
WHERE Reviews.ProductID = 1;

-- 6. فهرست تمام کاربران با آدرس‌های مربوطه:
SELECT Users.Username, Users.Email, Addresses.Street, Addresses.City, Addresses.State, Addresses.PostalCode, Addresses.Country
FROM Users
JOIN Addresses ON Users.UserID = Addresses.UserID;

-- 7. بازیابی مقدار کل هزینه شده توسط هر کاربر در تمامی سفارشاتشان:
SELECT Users.Username, SUM(OrderDetails.Quantity * Products.Price) AS TotalSpent
FROM Users
JOIN Orders ON Users.UserID = Orders.UserID
JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
JOIN Products ON OrderDetails.ProductID = Products.ProductID
GROUP BY Users.Username;

-- 8. دریافت تاریخچه سفارشات با جزئیات اطلاعات محصول برای یک کاربر خاص:
SELECT Orders.OrderID, Orders.OrderDate, Products.ProductName, OrderDetails.Quantity, (OrderDetails.Quantity * Products.Price) AS TotalPrice
FROM Orders
JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
JOIN Products ON OrderDetails.ProductID = Products.ProductID
WHERE Orders.UserID = 1
ORDER BY Orders.OrderDate DESC;

-- 9. فهرست محصولات به همراه تعداد کل دفعات سفارش شده:
SELECT Products.ProductName, SUM(OrderDetails.Quantity) AS TotalOrdered
FROM Products
JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID
GROUP BY Products.ProductName
ORDER BY TotalOrdered DESC;

-- 10. بازیابی تمام کاربران که هیچ سفارشی ثبت نکرده‌اند:
SELECT Users.Username, Users.Email
FROM Users
LEFT JOIN Orders ON Users.UserID = Orders.UserID
WHERE Orders.UserID IS NULL;