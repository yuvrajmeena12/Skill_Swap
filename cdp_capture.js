const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const userDataDir = path.join(__dirname, 'edge_capture_profile');
const outputDir = path.join(__dirname, 'ppt_assets');

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Load auth token
const authData = JSON.parse(fs.readFileSync(path.join(__dirname, 'auth_token.json'), 'utf8'));

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function sendCDP(ws, method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = Math.floor(Math.random() * 1000000);
    const handler = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id === id) {
        ws.removeEventListener('message', handler);
        if (msg.error) reject(msg.error);
        else resolve(msg.result);
      }
    };
    ws.addEventListener('message', handler);
    ws.send(JSON.stringify({ id, method, params }));
  });
}

async function main() {
  console.log('Launching Edge...');
  const proc = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=9222',
    `--user-data-dir=${userDataDir}`,
    '--window-size=1280,800',
    'about:blank'
  ]);

  await sleep(2500);

  try {
    const verRes = await fetch('http://localhost:9222/json/list');
    const pages = await verRes.json();
    const page = pages[0];
    console.log('Page target:', page.id);

    const ws = new WebSocket(page.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);
    console.log('Connected to WebSocket!');

    await sendCDP(ws, 'Page.enable');
    await sendCDP(ws, 'Runtime.enable');
    await sendCDP(ws, 'Emulation.setDeviceMetricsOverride', {
      width: 1280,
      height: 800,
      deviceScaleFactor: 1.5,
      mobile: false
    });

    // Capture Landing Page
    console.log('Capturing Landing Page Hero...');
    await sendCDP(ws, 'Page.navigate', { url: 'http://localhost:5173/' });
    await sleep(2000);
    let shot = await sendCDP(ws, 'Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(outputDir, '01_landing_hero.png'), Buffer.from(shot.data, 'base64'));

    // Capture Landing Page features (scroll down)
    console.log('Capturing Landing Features...');
    await sendCDP(ws, 'Runtime.evaluate', { expression: 'window.scrollTo(0, 750);' });
    await sleep(1000);
    shot = await sendCDP(ws, 'Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(outputDir, '02_landing_features.png'), Buffer.from(shot.data, 'base64'));

    // Capture Login Page
    console.log('Capturing Login Page...');
    await sendCDP(ws, 'Page.navigate', { url: 'http://localhost:5173/login' });
    await sleep(1500);
    shot = await sendCDP(ws, 'Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(outputDir, '03_login_page.png'), Buffer.from(shot.data, 'base64'));

    // Capture Register Page
    console.log('Capturing Register Page...');
    await sendCDP(ws, 'Page.navigate', { url: 'http://localhost:5173/register' });
    await sleep(1500);
    shot = await sendCDP(ws, 'Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(outputDir, '04_register_page.png'), Buffer.from(shot.data, 'base64'));

    // Inject Auth state
    console.log('Injecting Auth Credentials...');
    const injectCode = `
      localStorage.setItem('token', ${JSON.stringify(authData.token)});
      localStorage.setItem('user', ${JSON.stringify(JSON.stringify(authData))});
    `;
    await sendCDP(ws, 'Runtime.evaluate', { expression: injectCode });

    // Capture Dashboard
    console.log('Capturing Dashboard...');
    await sendCDP(ws, 'Page.navigate', { url: 'http://localhost:5173/dashboard' });
    await sleep(2500);
    shot = await sendCDP(ws, 'Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(outputDir, '05_dashboard.png'), Buffer.from(shot.data, 'base64'));

    // Capture My Skills
    console.log('Capturing My Skills...');
    await sendCDP(ws, 'Page.navigate', { url: 'http://localhost:5173/my-skills' });
    await sleep(2500);
    shot = await sendCDP(ws, 'Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(outputDir, '06_my_skills.png'), Buffer.from(shot.data, 'base64'));

    // Capture Explore Skills
    console.log('Capturing Explore Skills...');
    await sendCDP(ws, 'Page.navigate', { url: 'http://localhost:5173/explore' });
    await sleep(2500);
    shot = await sendCDP(ws, 'Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(outputDir, '07_explore_skills.png'), Buffer.from(shot.data, 'base64'));

    // Capture Smart Match
    console.log('Capturing Smart Match...');
    await sendCDP(ws, 'Page.navigate', { url: 'http://localhost:5173/smart-match' });
    await sleep(2500);
    shot = await sendCDP(ws, 'Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(outputDir, '08_smart_match.png'), Buffer.from(shot.data, 'base64'));

    // Capture My Swaps
    console.log('Capturing My Swaps...');
    await sendCDP(ws, 'Page.navigate', { url: 'http://localhost:5173/my-swaps' });
    await sleep(2000);
    shot = await sendCDP(ws, 'Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(outputDir, '09_my_swaps.png'), Buffer.from(shot.data, 'base64'));

    ws.close();
    console.log('All 9 page screenshots captured successfully!');
  } catch (err) {
    console.error('Error during CDP capture:', err);
  } finally {
    proc.kill();
  }
}

main();
