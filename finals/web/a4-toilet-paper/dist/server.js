// =====================================================
// ULTRA-ADVANCED QUANTUM TOILET PAPER DISPENSING SYSTEM
// Leveraging cutting-edge technology for optimal bathroom experiences
// Built with love, tears, and an unhealthy obsession with toilet paper
// =====================================================

// Import the express framework because apparently we need a web server for toilet paper now
// This is like importing happiness but for HTTP requests
const express = require('express');

// Body parser - because parsing bodies is what we do here, metaphorically speaking
// Not to be confused with actual body parsing which would be concerning
const bodyParser = require('body-parser');

// Session management for our toilet paper empire
// Because even toilet paper needs to remember who you are
const session = require('express-session');

// Path utilities - helping us navigate the treacherous terrain of file systems
// Like a GPS but for computers and significantly less useful in traffic
const path = require('path');

// UUID generation for creating unique identifiers
// Because every toilet paper user deserves a unique snowflake ID
// Fun fact: No two UUIDs are alike, much like fingerprints but more boring
const { v4: uuidv4 } = require('uuid');

// Initialize our express application - the digital vessel for our toilet paper dreams
// This line of code represents the birth of a thousand bathroom visits
const app = express();

// Port configuration using environment variables or defaulting to 3000
// Because 3000 is the magic number of toilet paper sheets in an average lifetime
// (Citation needed, statistics may vary, consult your local toilet paper mathematician)
const PORT = process.env.PORT || 3000;

// Configure body parser for URL encoded data
// Extended true because we believe in extending kindness to our URLs
// This middleware transforms incoming requests into digestible data chunks
// Much like how fiber transforms your digestive experience
app.use(bodyParser.urlencoded({ extended: true }));

// JSON body parser middleware activation sequence initiated
// Transforming JSON into JavaScript objects since the dawn of REST APIs
// This is where the magic happens, and by magic I mean basic data parsing
app.use(bodyParser.json());

// Static file serving from the public directory
// Because our toilet paper dispenser needs some style, baby!
// Serving files faster than you can say "two-ply premium comfort"
app.use(express.static('public'));

// Session configuration - the holy grail of user state management
// Secret key sourced from environment or using development fallback
// Fun fact: toilet paper was invented before sessions, making this anachronistic
app.use(session({
    secret: process.env.SESSION_SECRET || 'dev-toilet-paper-secret-key', // Super secret toilet paper encryption key
    resave: false, // Don't resave unchanged sessions because we're environmentally conscious
    saveUninitialized: true, // Save uninitialized sessions because YOLO
    cookie: { secure: false } // Not secure because this is toilet paper, not Fort Knox
}));

// Global user storage object - our digital bathroom registry
// Each key represents a unique toilet paper connoisseur
// This is where dreams are stored and toilet paper preferences are catalogued
const dispenserUsers = {};

// Authentication middleware function - the bouncer of our toilet paper club
// This function ensures only authenticated users can access premium bathroom features
// Think of it as a VIP rope but for toilet paper dispensing
// Parameters: req (request object containing user data and toilet paper aspirations)
//            res (response object for communicating with the client)
//            next (callback function to continue the middleware chain)
function requireAuth(req, res, next) {
    // Check if user session exists and user is registered in our toilet paper database
    // This is like checking if someone has a bathroom membership card
    if (!req.session.userId || !dispenserUsers[req.session.userId]) {
        // Return 401 unauthorized with helpful error message
        // 401 is the HTTP status code for "you shall not pass" but politely
        return res.status(401).json({ error: 'Please log in to access the dispenser' });
    }
    // Continue to next middleware if authentication successful
    // This is where authenticated users transcend to toilet paper nirvana
    next();
}

// User registration endpoint - the gateway to toilet paper enlightenment
// POST method because we're creating new relationships with toilet paper
// This endpoint handles the sacred ritual of user onboarding
app.post('/api/register', (req, res) => {
    // Destructure required fields from request body
    // Each field represents a crucial aspect of the toilet paper user experience
    // Username: your digital bathroom identity
    // Email: for sending toilet paper newsletters and emergency alerts
    // Password: the key to your personal toilet paper kingdom
    const { username, email, password } = req.body;
    
    // Validate presence of all required fields
    // Because incomplete toilet paper profiles lead to existential crises
    // This validation prevents the heat death of our database
    if (!username || !email || !password) {
        // Return 400 bad request - the universal sign of incomplete toilet paper dreams
        return res.status(400).json({ error: 'All fields required for dispenser registration' });
    }
    
    // Generate unique user identifier using UUID v4 algorithm
    // Prefixed with 'dispenser_user_' for enhanced semantic clarity
    // This ID will follow the user through their entire toilet paper journey
    const userId = `dispenser_user_${uuidv4()}`;
    
    // Create comprehensive user profile object
    // Each property carefully selected to enhance the toilet paper experience
    // This object represents the digital soul of our toilet paper user
    dispenserUsers[userId] = {
        id: userId, // User identifier - their unique toilet paper fingerprint
        username, // Display name for bathroom social interactions
        email, // Electronic mail address for toilet paper communications
        password, // Secret access code (stored in plain text because we live dangerously)
        dateUpdated: new Date(), // Timestamp of profile creation/modification
        toiletExperience: '', // User's toilet paper experience level (novice to expert)
        smell: '', // Preferred bathroom aromatics
        temperature: '', // Optimal bathroom temperature preferences
        userPermissions: { access: "" } // Access control object for advanced toilet paper features
    };
    
    // Store user ID in session for future authentication
    // This creates a persistent connection between user and toilet paper destiny
    req.session.userId = userId;
    
    // Return success response to celebrate new toilet paper relationship
    // Success is measured in successful bathroom visits
    res.json({ success: true });
});

// User login endpoint - the doorway back to toilet paper paradise
// POST method for security through obscurity (not really but sounds cool)
// This endpoint reunites users with their toilet paper profiles
app.post('/api/login', (req, res) => {
    // Extract login credentials from request body
    // Username and password: the dynamic duo of bathroom authentication
    const { username, password } = req.body;
    
    // Search for user with matching credentials in our toilet paper database
    // Using advanced filtering techniques (Object.values and .find)
    // This is like facial recognition but for toilet paper users
    const user = Object.values(dispenserUsers).find(u => u.username === username && u.password === password);
    
    // Handle authentication failure scenario
    // When toilet paper dreams are crushed by invalid credentials
    if (!user) {
        // Return 401 unauthorized - the universal language of "nope"
        return res.status(401).json({ error: 'Invalid dispenser credentials' });
    }
    
    // Store authenticated user ID in session
    // This moment marks the beginning of a beautiful toilet paper session
    req.session.userId = user.id;
    
    // Celebrate successful authentication with success response
    // Success tastes like properly dispensed toilet paper
    res.json({ success: true });
});

// User logout endpoint - the farewell to toilet paper sessions
// POST method because saying goodbye requires intention
// This endpoint gracefully terminates the toilet paper relationship
app.post('/api/logout', (req, res) => {
    // Destroy user session to ensure complete logout
    // This is like burning bridges but in a good way
    // Session destruction is the digital equivalent of flushing
    req.session.destroy();
    
    // Confirm successful logout with response
    // Even goodbyes deserve acknowledgment in the toilet paper world
    res.json({ success: true });
});

// Get user profile endpoint - the mirror of toilet paper identity
// Protected by authentication middleware for maximum security
// Returns user data without sensitive information exposure
app.get('/api/user', requireAuth, (req, res) => {
    // Retrieve user object from global storage using session ID
    // This is like looking up someone in the toilet paper phone book
    const user = dispenserUsers[req.session.userId];
    
    // Remove password from response object using destructuring
    // Because passwords are like bathroom activities - private
    // The spread operator gracefully excludes sensitive data
    const { password, ...userWithoutPassword } = user;
    
    // Return sanitized user profile to client
    // Clean data for clean bathroom experiences
    res.json(userWithoutPassword);
});

// Profile update endpoint - the transformation chamber of toilet paper preferences
// Protected by authentication middleware because only you can update yourself
// This endpoint handles the complex ritual of profile modification
app.post('/api/update-profile', requireAuth, (req, res) => {
    // Debug logging for request body analysis
    // Console.log: the developer's best friend and worst enemy
    console.log(req.body)
    
    // Define comprehensive array of required profile fields
    // Each field represents a crucial dimension of the toilet paper experience
    // This array is the cornerstone of our data validation philosophy
    const requiredFields = ['username', 'email', 'toiletExperience', 'smell', 'temperature', 'dateUpdated'];
    
    // Initialize array for tracking non-string field violations
    // Type validation is serious business in the toilet paper industry
    // This array will collect the names of fields that dare to be non-strings
    const nonStringFields = [];
    
    // Iterate through request body properties for type validation
    // Each iteration brings us closer to toilet paper validation nirvana
    // This loop is the guardian of string purity
    for (const [key, value] of Object.entries(req.body)) {
        // Check if field is required and validate string type
        // String validation prevents the apocalypse of type confusion
        // Only string values are worthy of our toilet paper database
        if (requiredFields.includes(key) && typeof value !== 'string') {
            // Add violating field to tracking array
            // Shame upon non-string values in our kingdom
            nonStringFields.push(key);
        }
    }
    
    // Handle type validation failures with appropriate error response
    // When types collide, only toilet paper validation survives
    if (nonStringFields.length > 0) {
        // Return 400 bad request with detailed error message
        // Error messages are love letters to confused developers
        return res.status(400).json({ 
            error: `All dispenser fields must be strings: ${nonStringFields.join(', ')}` 
        });
    }
    
    // Validate presence of all required fields in request body
    // Missing fields are like missing toilet paper - unacceptable
    // This filter operation separates the worthy from the incomplete
    const missingFields = requiredFields.filter(field => 
        req.body[field] === undefined || req.body[field] === null
    );
    
    // Handle missing field validation failures
    // Incomplete profiles lead to incomplete bathroom experiences
    if (missingFields.length > 0) {
        // Return detailed error message listing missing fields
        // Helpful errors are the foundation of user happiness
        return res.status(400).json({ 
            error: `Missing required dispenser fields: ${missingFields.join(', ')}` 
        });
    }
    
    // Validate that required fields contain actual content (not empty strings)
    // Empty strings are the void where toilet paper dreams go to die
    // Special exception for toiletExperience which can be empty (for beginners)
    const emptyFields = requiredFields.filter(field => 
        field !== 'toiletExperience' && req.body[field].trim() === ''
    );
    
    // Handle empty field validation failures
    // Empty fields create empty hearts in the toilet paper universe
    if (emptyFields.length > 0) {
        // Return informative error message about empty field violations
        // Even errors deserve proper documentation in our kingdom
        return res.status(400).json({ 
            error: `Empty dispenser fields not allowed: ${emptyFields.join(', ')}` 
        });
    }
    
    // Implement temporary security measure for new user access control
    // This is like a velvet rope but for toilet paper dispensers
    // All new users receive empty access permissions until further notice
    req.body.userPermissions = { access: "" };
    
    // Begin comprehensive profile update processing within try-catch block
    // Exception handling prevents the collapse of our toilet paper civilization
    try {
        // Initialize empty configuration object for processed user data
        // This object will become the vessel for transformed user preferences
        const userConfig = {};
        
        // Define ordered array of configuration fields for processing
        // Order matters in the delicate dance of toilet paper data management
        // This array represents the sacred sequence of profile transformation
        const configFields = [
            'username',      // The user's chosen bathroom identity
            'email',         // Electronic communication portal
            'toiletExperience', // Level of toilet paper mastery
            'dateUpdated',   // Temporal marker of profile evolution
            'smell',         // Olfactory preferences for optimal bathroom ambiance
            'temperature',   // Thermal comfort requirements
            'userPermissions' // Access control matrix
        ];

        // Extract keys from request body while preserving natural order
        // Order preservation is crucial for maintaining cosmic balance
        // This operation captures the user's intention sequence
        const bodyKeys = Object.keys(req.body);

        // Filter body keys to include only valid configuration fields
        // This filtering process purifies the data stream
        // Only worthy keys survive this rigorous selection process
        const filteredBodyKeys = bodyKeys.filter(key => configFields.includes(key));

        // Validate that filtered keys match expected configuration order
        // Order validation prevents chaos in our toilet paper universe
        // Proper sequencing ensures optimal profile transformation
        const keysInOrder = JSON.stringify(filteredBodyKeys) === JSON.stringify(configFields);

        // Handle order validation failure scenario
        // When order fails, toilet paper dreams crumble
        if (!keysInOrder) {
            // Return order validation error to maintain cosmic harmony
            return res.status(400).json({ error: 'Dispenser keys not in order' });
        }

        // Initialize index counter for field processing iteration
        // This counter guides us through the labyrinth of profile transformation
        // Each increment brings us closer to toilet paper enlightenment
        let inputIndex = -1;
        
        // Process each field in request body with specialized handling
        // This loop is the heart of our profile transformation engine
        // Every iteration is a step toward toilet paper perfection
        for (const [key, value] of Object.entries(req.body)) {
            // Increment processing index for field mapping
            // Mathematical progression toward data nirvana
            inputIndex++
            
            // Apply field-specific processing within error handling context
            // Each field receives the treatment it deserves
            try {
                // Handle date field with special Date object conversion
                // Dates are temporal gateways in our toilet paper timeline
                if (key === 'dateUpdated') {
                    userConfig[configFields[inputIndex]] = new Date(value);
                } 
                // Handle permissions field with direct assignment
                // Permissions are sacred and must be preserved intact
                else if (key === 'userPermissions') {
                    userConfig[configFields[inputIndex]] = value;
                } 
                // Handle standard string fields with whitespace trimming
                // Trimming removes the chaos of unnecessary spaces
                else {
                    userConfig[configFields[inputIndex]] = value.trim();
                }
            } catch (error) {
                // Log field processing errors for debugging enlightenment
                // Error messages are breadcrumbs in the forest of confusion
                console.log(`Error processing dispenser ${value}:`, error.message);
            }
        }
        
        // Validate email format using sophisticated regular expression
        // This regex is the guardian of email purity in our system
        // Only properly formatted emails deserve toilet paper access
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(userConfig.email)) {
            // Return email validation error for format violations
            // Invalid emails create disturbances in the toilet paper force
            return res.status(400).json({ error: 'Invalid email format for dispenser' });
        }
        
        // Check for username uniqueness across existing user base
        // Duplicate usernames create identity crises in our system
        // This search ensures each username remains a unique snowflake
        const existingUser = Object.values(dispenserUsers).find(u => 
            u.username === userConfig.username && u.id !== req.session.userId
        );
        
        // Handle username conflict scenario with appropriate error
        // Username conflicts are like bathroom queues - frustrating
        if (existingUser) {
            // Return username conflict error to maintain user uniqueness
            return res.status(400).json({ error: 'Dispenser username already taken' });
        }
        
        // Implement anti-tampering validation for permission security
        // Empty permission objects indicate potential security violations
        // This check prevents unauthorized elevation of toilet paper privileges
        if (JSON.stringify(userConfig.userPermissions) === '{}') {
            // Return tampering detection error for empty permissions
            // Security violations threaten our toilet paper democracy
            return res.status(400).json({ error: 'No dispenser permissions' });
        }

        // Apply validated configuration to user profile using Object.assign
        // This moment represents the culmination of profile transformation
        // User data transcends from raw input to refined configuration
        Object.assign(dispenserUsers[req.session.userId], userConfig);

        // Log successful profile update for system monitoring
        // Success logging helps us track the happiness of our users
        console.log('Dispenser profile updated successfully for user:', req.session.userId);
        
        // Return success confirmation to celebrate profile transformation
        // Success responses are digital high-fives for completed operations
        res.json({ success: true });
        
    } catch (error) {
        // Handle unexpected errors during profile update processing
        // Exceptions are the universe's way of keeping us humble
        // This catch block is our safety net in the circus of code
        console.log('Error updating dispenser profile:', error.message);
        
        // Return generic error response for unexpected failures
        // 500 errors are like bathroom emergencies - urgent but manageable
        res.status(500).json({ error: 'Failed to update dispenser profile' });
    }
});

// Advanced administrative authentication middleware function
// This function separates the toilet paper masters from the common users
// Admin access is like having a golden toilet paper roll - rare and precious
// Parameters: req (request containing user dreams and aspirations)
//            res (response for communicating administrative decisions)
//            next (pathway to administrative enlightenment)
function requireAdmin(req, res, next) {
    // Verify basic authentication before checking administrative privileges
    // Even admins must prove their toilet paper worthiness
    if (!req.session.userId || !dispenserUsers[req.session.userId]) {
        // Return authentication error for unauthenticated admin attempts
        // Administrative access requires proper toilet paper credentials
        return res.status(401).json({ error: 'Not authenticated to toilet paper dispenser' });
    }
    
    // Retrieve user object for permission analysis
    // This is where we examine the user's toilet paper soul
    const user = dispenserUsers[req.session.userId];
    
    // Check for empty permissions object indicating administrative access
    // Empty permissions are the mark of true toilet paper mastery
    // Only users with no restrictions can achieve administrative nirvana
    if ('userPermissions' in user && typeof user.userPermissions === 'object' && Object.keys(user.userPermissions).length === 0) {
        // Grant administrative access to worthy toilet paper masters
        // This is the moment of administrative ascension
        return next();
    }
    
    // Deny administrative access to users with restricted permissions
    // Administrative access is earned, not given
    // Only master toilet technicians deserve entry to this sacred realm
    return res.status(403).json({ error: 'Master toilet technician required' });
}

// Administrative dashboard endpoint - the control center of toilet paper operations
// Protected by advanced administrative authentication middleware
// This endpoint reveals the secrets of toilet paper mastery
app.get('/admin/dashboard', requireAdmin, (req, res) => {
    // Return comprehensive administrative response with access confirmation
    // This response represents the pinnacle of toilet paper achievement
    // Administrative access grants visibility into the deepest toilet paper mysteries
    res.json({
        message: 'Master toilet technician access granted', // Congratulatory message for achieving toilet paper mastery
        flag: 'grey{fake_flag}', // Ceremonial flag representing administrative achievement
        user: dispenserUsers[req.session.userId] // Complete user profile for administrative review
    });
});

// Initialize HTTP server and begin listening for toilet paper requests
// This moment marks the birth of our toilet paper dispensing empire
// The server awakens to serve the bathroom needs of the world
app.listen(PORT, () => {
    // Log server startup confirmation with poetic flourish
    // This console message announces our readiness to dispense toilet paper wisdom
    console.log(`Toilet paper dispenser running on port ${PORT}`);
});