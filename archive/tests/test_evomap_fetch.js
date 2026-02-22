const crypto = require('crypto');
const https = require('https');

function request(options, data) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          resolve(body);
        }
      });
    });
    req.on('error', reject);
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
}

async function testFetch() {
  const nodeId = 'node_5dfb234713e2d1e7';
  const timestamp = new Date().toISOString();
  const messageId = 'msg_' + Date.now() + '_' + Math.floor(Math.random() * 100000);

  console.log('=== Testing EvoMap Fetch ===');
  console.log('Using Node ID:', nodeId);
  console.log();

  // Test fetch
  console.log('Testing /a2a/fetch...');
  const fetchPayload = {
    protocol: 'gep-a2a',
    protocol_version: '1.0.0',
    message_type: 'fetch',
    message_id: messageId,
    sender_id: nodeId,
    timestamp: timestamp,
    payload: {
      asset_type: 'Capsule',
      query: 'openclaw',
      limit: 5
    }
  };

  const fetchOptions = {
    hostname: 'evomap.ai',
    port: 443,
    path: '/a2a/fetch',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  };

  try {
    const fetchResult = await request(fetchOptions, fetchPayload);
    console.log('Fetch result:', JSON.stringify(fetchResult, null, 2));
  } catch (e) {
    console.error('Fetch error:', e.message);
  }

  console.log();
}

testFetch().catch(console.error);
