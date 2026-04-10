const https = require('https');

// A developer did this to bypass a local firewall error, 
// but accidentally left it in production. It completely disables SSL verification globally.
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

function fetchUserData(url) {
    // This request is now vulnerable to Man-In-The-Middle (MITM) attacks
    return https.get(url, (res) => {
        console.log("Data fetched securely... maybe.");
    });
}
module.exports = { fetchUserData };