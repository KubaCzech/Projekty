// // Simple Online Store using Node.js, Express, and EJS

// const express = require('express');
// const session = require('express-session');
// const bodyParser = require('body-parser');
// const mysql = require('mysql2/promise');

// const app = express();
// const PORT = 3000;

// // Database setup
// const dbConfig = {
//     host: 'localhost',   // MySQL host
//     user: 'root',        // MySQL user
//     password: '',        // MySQL password
//     database: 'online_store', // Database name
//   };

// // Middleware setup
// app.use(bodyParser.urlencoded({ extended: true }));
// app.use(
//   session({
//     secret: 'secure-key',
//     resave: false,
//     saveUninitialized: true,
//   })
// );
// app.set('view engine', 'ejs');

// // Connect to database
// let db;
// (async () => {
//   try {
//     db = await mysql.createConnection(dbConfig);
//     console.log('Connected to the database!');

//     // Fetch products from the database
//     const [products] = await db.execute('SELECT * FROM products');
//     console.log('Products:', products);

//     // Close the connection
//     // await db.end();
//   } catch (error) {
//     console.error('Database connection failed:', error);
//   }
// })();

// // Initialize session cart
// app.use((req, res, next) => {
//   if (!req.session.cart) req.session.cart = [];
//   next();
// });

// // Routes

// // Main page - Display products
// app.get('/', async (req, res) => {
//   const [products] = await db.execute('SELECT * FROM products');
//   res.render('index', { products, cart: req.session.cart });
// });

// // Add product to cart
// app.post('/add-to-cart', (req, res) => {
//   const productId = req.body.productId;
// //   if (!req.session.cart.includes(productId)) {
// //     req.session.cart.push(productId);
// //   }
//     req.session.cart.push(productId);
//     console.log("Added product", productId)
//     console.log(req.session.cart)
//   res.redirect('/');
// });

// // View cart
// app.get('/cart', async (req, res) => {
//   if (req.session.cart.length === 0) return res.render('cart', { cartItems: [], message: '' });

//   const placeholders = req.session.cart.map(() => '?').join(',');
//   const [cartItems] = await db.execute(
//     `SELECT * FROM products WHERE id IN (${placeholders})`,
//     req.session.cart
//   );
//   res.render('cart', { cartItems, message: '' });
// });

// // Remove product from cart
// app.post('/remove-from-cart', (req, res) => {
//   const productId = req.body.productId;
//   req.session.cart = req.session.cart.filter((id) => id !== productId);
//   res.redirect('/cart');
// });

// // Finalize purchase
// app.post('/checkout', async (req, res) => {
//   try {
//     const placeholders = req.session.cart.map(() => '?').join(',');
//     const [products] = await db.execute(
//       `SELECT * FROM products WHERE id IN (${placeholders})`,
//       req.session.cart
//     );

//     // Check stock availability
//     for (const product of products) {
//       if (product.quantity <= 0) {
//         return res.render('cart', {
//           cartItems: products,
//           message: `${product.name} is out of stock!`,
//         });
//       }
//     }

//     // Update stock and finalize purchase
//     for (const product of products) {
//       await db.execute('UPDATE products SET quantity = quantity - 1 WHERE id = ?', [product.id]);
//     }

//     req.session.cart = []; // Clear cart
//     res.redirect('/?message=Purchase successful!');
//   } catch (error) {
//     console.error(error);
//     res.render('cart', { cartItems: [], message: 'An error occurred during checkout.' });
//   }
// });

// // Cancel purchase
// app.post('/cancel', (req, res) => {
//   req.session.cart = []; // Clear cart
//   res.redirect('/');
// });

// // Start server
// app.listen(PORT, () => {
//   console.log(`Server running on http://localhost:${PORT}`);
// });

// // EJS Templates:
// // 1. index.ejs - Displays product list with "Add to Cart" buttons
// // 2. cart.ejs - Displays shopping cart with "Remove", "Checkout", and "Cancel" buttons

const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const mysql = require('mysql2');
const app = express();
const PORT = 3000;


app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(
  session({
    secret: 'secretKey',
    resave: false,
    saveUninitialized: true,
  })
);
  
app.use((req, res, next) => {
    console.log(`Session ID: ${req.sessionID}`);
    next();
});
  



// Database connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'my_store',
});

db.connect((err) => {
  if (err) throw err;
  console.log('Connected to MySQL database!');
});

// Routes

// Main page displaying products
app.get('/', (req, res) => {
  db.query(
    'SELECT id, name, description, CAST(price AS DECIMAL(10, 2)) AS price, quantity FROM products',
    (err, results) => {
      if (err) throw err;
      res.render('index', { products: results, message: req.session.message });
      req.session.message = null; 
    }
  );
});

// Add to cart
app.post('/add-to-cart', (req, res) => {
  const productId = parseInt(req.body.productId, 10);

  db.query('SELECT * FROM products WHERE id = ?', [productId], (err, results) => {
    if (err) throw err;

    const product = results[0];
    if (product && product.quantity > 0) {
      if (!req.session.cart) req.session.cart = [];

      const existingProduct = req.session.cart.find((item) => item.id === productId);
      let newQuantity = 1;

      if (existingProduct) {
        newQuantity = existingProduct.cartQuantity + 1;
      }

      if (newQuantity > product.quantity) {
        req.session.message = 'Not enough stock available.';
      } else {
        if (existingProduct) {
          existingProduct.cartQuantity = newQuantity;
        } else {
          req.session.cart.push({
            id: productId,
            name: product.name,
            price: product.price,
            cartQuantity: 1,
          });
        }

        req.session.message = 'Item added to cart!';
      }
    } else {
      req.session.message = 'This item is out of stock.';
    }

    res.redirect('/');
  });
});


// View shopping cart
app.get('/cart', (req, res) => {
  const cart = req.session.cart || [];
  const totalPrice = cart.reduce((total, item) => total + item.price * item.cartQuantity, 0);

  res.render('cart', { cartItems: cart, totalPrice });
});

// Remove item from cart
app.post('/remove-from-cart', (req, res) => {
  const productId = parseInt(req.body.productId, 10);
  req.session.cart = req.session.cart.filter((item) => item.id !== productId);
  res.redirect('/cart');
});


// Checkout with lock
const asyncLock = new (require('async-lock'))();

app.post('/checkout', (req, res) => {
  const cart = req.session.cart || [];

  if (cart.length === 0) {
    req.session.message = 'Your cart is empty!';
    return res.redirect('/cart');
  }

  asyncLock.acquire('checkout', (done) => {
    setTimeout(() => {
      db.beginTransaction((err) => {
        if (err) throw err;

        const productIds = cart.map((item) => item.id);
        const placeholders = productIds.map(() => '?').join(',');

        db.query(
          `SELECT id, quantity FROM products WHERE id IN (${placeholders}) FOR UPDATE`,
          productIds,
          (err, results) => {
            if (err) return db.rollback(() => { throw err; });

            const insufficientStock = cart.some((item) => {
              const product = results.find((p) => p.id === item.id);
              return !product || product.quantity < item.cartQuantity;
            });

            if (insufficientStock) {
              req.session.message = 'Some items are out of stock.';
              return db.rollback(() => res.redirect('/')); // Redirect to main page
            }

            const updates = cart.map((item) => {
              return new Promise((resolve, reject) => {
                db.query(
                  'UPDATE products SET quantity = quantity - ? WHERE id = ?',
                  [item.cartQuantity, item.id],
                  (err) => {
                    if (err) reject(err);
                    resolve();
                  }
                );
              });
            });

            Promise.all(updates)
              .then(() => {
                db.commit((err) => {
                  if (err) return db.rollback(() => { throw err; });

                  req.session.cart = []; // Clear the cart
                  req.session.message = 'Purchase successful!';
                  res.redirect('/');
                });
              })
              .catch((err) => {
                db.rollback(() => {
                  req.session.message = err.message || 'Purchase failed!';
                  res.redirect('/cart');
                });
              })
              .finally(() => {
                done(); // Release the lock
              });
          }
        );
      });
    }, 10000); // Sleep to simulate the proccess of a transaction 
  }, (err) => {
    if (err) {
      req.session.message = 'Another checkout process is currently in progress, please try again later.';
      res.redirect('/cart');
    }
  });
});


// Cancel purchase
app.post('/cancel', (req, res) => {
  req.session.cart = [];
  req.session.message = 'Purchase cancelled.';
  res.redirect('/');
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});