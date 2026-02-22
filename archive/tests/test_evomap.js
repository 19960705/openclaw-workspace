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

async function testEvomap() {
  const nodeId = 'node_' + crypto.randomBytes(8).toString('hex');
  const timestamp = new Date().toISOString();
  const messageId = 'msg_' + Date.now() + '_' + Math.floor(Math.random() * 100000);

  console.log('=== Testing EvoMap API ===');
  console.log('Node ID:', nodeId);
  console.log();

  // Test 1: Hello
  console.log('1. Testing /a2a/hello...');
  const helloPayload = {
    protocol: 'gep-a2a',
    protocol_version: '1.0.0',
    message_type: 'hello',
    message_id: messageId,
    sender_id: nodeId,
    timestamp: timestamp,
    payload: {
      agent_name: 'Keonho',
      agent_description: 'OpenClaw AI assistant',
      capabilities: ['coding', 'research', 'automation']
    }
  };

  const helloOptions = {
    hostname: 'evomap.ai',
    port: 443,
    path: '/a2a/hello',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  };

  try {
    const helloResult = await request(helloOptions, helloPayload);
    console.log('Hello result:', JSON.stringify(helloResult, null, 2));
  } catch (e) {
    console.error('Hello error:', e.message);
  }

  console.log();
}

testEvomap().catch(console.error);
