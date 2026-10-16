// Bounded authored JSON codec probe; this is not a causal adapter.
let text = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { text += chunk; });
process.stdin.on('end', () => { process.stdout.write(JSON.stringify(JSON.parse(text))); });
