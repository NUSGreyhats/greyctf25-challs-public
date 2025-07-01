const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static('public'));
app.use(session({
    secret: process.env.SESSION_SECRET || 'dev-toilet-paper-secret-key',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }
}));

const dispenserUsers = {};

function requireAuth(req, res, next) {
    if (!req.session.userId || !dispenserUsers[req.session.userId]) {
        return res.status(401).json({ error: 'Please log in to access the dispenser' });
    }
    next();
}

app.post('/api/register', (req, res) => {
    const { username, email, password } = req.body;
    
    if (!username || !email || !password) {
        return res.status(400).json({ error: 'All fields required for dispenser registration' });
    }
    
    const userId = `dispenser_user_${uuidv4()}`;
    dispenserUsers[userId] = {
        id: userId,
        username,
        email,
        password,
        dateUpdated: new Date(),
        toiletExperience: '',
        smell: '',
        temperature: '',
        userPermissions: { access: "" }
    };
    
    req.session.userId = userId;
    res.json({ success: true });
});

app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    
    const user = Object.values(dispenserUsers).find(u => u.username === username && u.password === password);
    
    if (!user) {
        return res.status(401).json({ error: 'Invalid dispenser credentials' });
    }
    
    req.session.userId = user.id;
    res.json({ success: true });
});

app.post('/api/logout', (req, res) => {
    req.session.destroy();
    res.json({ success: true });
});

app.get('/api/user', requireAuth, (req, res) => {
    const user = dispenserUsers[req.session.userId];
    const { password, ...userWithoutPassword } = user;
    res.json(userWithoutPassword);
});

app.post('/api/update-profile', requireAuth, (req, res) => {
    console.log(req.body)
    // Define required fields for dispenser profile update
    const requiredFields = ['username', 'email', 'toiletExperience', 'smell', 'temperature', 'dateUpdated'];
    
    // Validate that all fields in request body are strings
    const nonStringFields = [];
    for (const [key, value] of Object.entries(req.body)) {
        if (requiredFields.includes(key) && typeof value !== 'string') {
            nonStringFields.push(key);
        }
    }
    
    if (nonStringFields.length > 0) {
        return res.status(400).json({ 
            error: `All dispenser fields must be strings: ${nonStringFields.join(', ')}` 
        });
    }
    
    // Check if all required fields are present
    const missingFields = requiredFields.filter(field => 
        req.body[field] === undefined || req.body[field] === null
    );
    
    if (missingFields.length > 0) {
        return res.status(400).json({ 
            error: `Missing required dispenser fields: ${missingFields.join(', ')}` 
        });
    }
    
    // Validate that none of the required fields are empty strings (except toiletExperience which can be empty)
    const emptyFields = requiredFields.filter(field => 
        field !== 'toiletExperience' && req.body[field].trim() === ''
    );
    
    if (emptyFields.length > 0) {
        return res.status(400).json({ 
            error: `Empty dispenser fields not allowed: ${emptyFields.join(', ')}` 
        });
    }
    
    // Temporary lock on all new dispenser users before we get the toilet up
    req.body.userPermissions = { access: "" };
    
    try {
        const userConfig = {};
        
        const configFields = [
            'username', 
            'email',
            'toiletExperience',
            'dateUpdated',
            'smell',
            'temperature',
            'userPermissions'
        ];

        // Get the keys from req.body in their current order
        const bodyKeys = Object.keys(req.body);

        // Filter to only the keys that exist in configFields, preserving order
        const filteredBodyKeys = bodyKeys.filter(key => configFields.includes(key));

        // Check if the filtered keys match the configFields order
        const keysInOrder = JSON.stringify(filteredBodyKeys) === JSON.stringify(configFields);

        if (!keysInOrder) {
            return res.status(400).json({ error: 'Dispenser keys not in order' });
        }

        let inputIndex = -1;
        
        for (const [key, value] of Object.entries(req.body)) {
            inputIndex++
            try {
                if (key === 'dateUpdated') {
                    userConfig[configFields[inputIndex]] = new Date(value);
                } else if (key === 'userPermissions') {
                    userConfig[configFields[inputIndex]] = value;
                } else {
                    userConfig[configFields[inputIndex]] = value.trim();
                }
            } catch (error) {
                console.log(`Error processing dispenser ${value}:`, error.message);
            }
        }
        
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(userConfig.email)) {
            return res.status(400).json({ error: 'Invalid email format for dispenser' });
        }
        
        const existingUser = Object.values(dispenserUsers).find(u => 
            u.username === userConfig.username && u.id !== req.session.userId
        );
        
        if (existingUser) {
            return res.status(400).json({ error: 'Dispenser username already taken' });
        }

        // Check for tampering
        if (JSON.stringify(userConfig.userPermissions) === '{}') {
            return res.status(400).json({ error: 'No dispenser permissions' });
        }

        Object.assign(dispenserUsers[req.session.userId], userConfig);

        console.log('Dispenser profile updated successfully for user:', req.session.userId);
        res.json({ success: true });
        
    } catch (error) {
        console.log('Error updating dispenser profile:', error.message);
        res.status(500).json({ error: 'Failed to update dispenser profile' });
    }
});

function requireAdmin(req, res, next) {
    if (!req.session.userId || !dispenserUsers[req.session.userId]) {
        return res.status(401).json({ error: 'Not authenticated to toilet paper dispenser' });
    }
    
    const user = dispenserUsers[req.session.userId];
    
    if ('userPermissions' in user && typeof user.userPermissions === 'object' && Object.keys(user.userPermissions).length === 0) {
        return next();
    }
    
    return res.status(403).json({ error: 'Master toilet technician required' });
}

app.get('/admin/dashboard', requireAdmin, (req, res) => {
    res.json({
        message: 'Master toilet technician access granted',
        flag: process.env.TOILET_FLAG || 'grey{lol}',
        user: dispenserUsers[req.session.userId]
    });
});

app.listen(PORT, () => {
    console.log(`Toilet paper dispenser running on port ${PORT}`);
});