const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = 3000;

// Default credentials (change these for your setup)
const ADMIN_USERNAME = 'admin';
const ADMIN_PASSWORD = 'a3spaaaa';
const FLAG = 'FLAG{c4m3r4_h4ck3d_5ucc355fully}';

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(session({
  secret: 'camera-secret-key',
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false } // Set to true if using HTTPS
}));

// Serve static files
app.use(express.static('public'));

// Authentication middleware
function requireAuth(req, res, next) {
  if (req.session.authenticated) {
    next();
  } else {
    res.redirect('/');
  }
}

// Routes
app.get('/', (req, res) => {
  if (req.session.authenticated) {
    res.redirect('/dashboard');
  } else {
    res.sendFile(path.join(__dirname, 'views', 'login.html'));
  }
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  
  if (username === ADMIN_USERNAME && password === ADMIN_PASSWORD) {
    req.session.authenticated = true;
    req.session.username = username;
    res.redirect('/dashboard');
  } else {
    res.redirect('/?error=Invalid credentials');
  }
});

app.get('/dashboard', requireAuth, (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'dashboard.html'));
});

app.get('/flag', requireAuth, (req, res) => {
  res.json({ flag: FLAG });
});

app.get('/logout', (req, res) => {
  req.session.destroy();
  res.redirect('/');
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`IoT Camera Portal running on port ${PORT}`);
  console.log(`Access via: http://camera.home (through reverse proxy)`);
  console.log(`Default credentials: ${ADMIN_USERNAME}/${ADMIN_PASSWORD}`);
});
